import dlt
import dlt.common
from datetime import datetime, timedelta
import os
import fire
import logging
from urllib.parse import urlparse, parse_qs
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.auth import BearerTokenAuth
from dlt.sources.helpers.rest_client.paginators import HeaderLinkPaginator

logger = logging.getLogger("dlt")


class GithubAPI:
    def __init__(self, access_token):
        self.client = RESTClient(
            base_url="https://api.github.com",
            auth=BearerTokenAuth(token=access_token),
            paginator=HeaderLinkPaginator(),
        )

    def _should_stop_pagination(self, response):
        rate_limit_remaining = int(response.headers["x-ratelimit-remaining"])
        reset_timestamp = int(response.headers["x-ratelimit-reset"])
        reset_time = datetime.fromtimestamp(reset_timestamp)
        time_remaining = reset_time - datetime.now()

        if rate_limit_remaining < 500:
            logger.warning(
                f"Rate limit is getting low ({rate_limit_remaining} remaining). Stopping pagination."
            )
            return True
        else:
            logger.info(
                f"Rate limit is {rate_limit_remaining} remaining, will reset in {time_remaining}"
            )
            return False

    def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 100,
        max_results: int = 100,
    ):
        url = "/search/repositories"
        params = {
            "sort": sort,
            "order": order,
            "per_page": per_page,
            "q": query,
        }
        total_results = 0
        for page in self.client.paginate(url, params=params, data_selector="items"):
            for repository in page:
                yield repository

                total_results += 1
                if total_results >= max_results:
                    break

    def get_repository(self, owner: str, name: str):
        url = f"repos/{owner}/{name}"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

    def get_stargazers(
        self,
        owner: str,
        name: str,
        per_page: int = 100,
        max_results: int = None,
        resource_state=None,
    ):
        resource_name = f"last_page_{owner}_{name}"
        last_page_cache = 1
        if resource_state is not None:
            last_page_cache = resource_state.setdefault(resource_name, 1)
        url = f"repos/{owner}/{name}/stargazers"
        params = {
            "per_page": per_page,
            "page": last_page_cache,
        }
        headers = {"Accept": "application/vnd.github.star+json"}
        total_results = 0
        for page in self.client.paginate(url, params=params, headers=headers):
            parsed_url = urlparse(page.request.url)
            query_params = parse_qs(parsed_url.query)
            if "page" in query_params and resource_state is not None:
                current_page = int(query_params["page"][0])
                resource_state[resource_name] = max(last_page_cache, int(current_page))
            stargazers = [
                {
                    "user__login": stargazer["user"]["login"],
                    "starred_at": stargazer["starred_at"],
                    "repository_full_name": f"{owner}/{name}",
                }
                for stargazer in page
            ]
            yield stargazers
            if self._should_stop_pagination(page.response):
                break
            total_results += len(page)
            if max_results is not None and total_results >= max_results:
                break


os.environ["RUNTIME__LOG_LEVEL"] = "INFO"
os.environ["EXTRACT__WORKERS"] = "4"


@dlt.source
def github_source(access_token=dlt.secrets.value):
    api = GithubAPI(access_token)

    @dlt.resource(write_disposition="merge", primary_key="id")
    def repositories():
        two_months_ago = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
        yield from api.search_repositories(f"created:>{two_months_ago} stars:>500")

    @dlt.transformer(
        parallelized=True,
        write_disposition="merge",
        primary_key=["user__login", "repository_full_name"],
    )
    def stargazers(repository):
        owner, name = repository["full_name"].split("/")
        resource_state = dlt.current.resource_state("stargazers")
        yield from api.get_stargazers(owner, name, resource_state=resource_state)

    return repositories, repositories | stargazers


def run():
    pipeline = dlt.pipeline(
        "github",
        destination=dlt.destinations.duckdb("data/github.duckdb"),
        dataset_name="raw",
    )

    load_info = pipeline.run(github_source())
    print(load_info)


if __name__ == "__main__":
    fire.Fire(run)
