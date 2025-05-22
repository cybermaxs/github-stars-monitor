# Github Stars Monitor : Never miss a new top starred repository

This project is a _simple_ pipeline to get the top starred newly created repositories from Github.

![demo](./docs/demo.gif)

Internally, the project is built with :
* [dlt](https://dlthub.com/) as ingestion tool.
* [DuckDB](https://duckdb.org/) as database.
* [dbt](https://www.dbt.com/) as transformation tool.
* [Evidence](https://evidence.dev/) as dashboard.

The pipeline is scheduled to run every day at 12:00 AM UTC and deployed to [Github pages](https://cybermaxs.github.io/github-stars-monitor/).

## Development

The project requires :
* Python 3.12
* uv for python packages.
* Nodejs (only for the visualization part)
* a Github Personal Access Token (PAT) to fetch the data from Github.

Common tasks are available in a `Makefile`.

```bash
make install
make run
```

## Feature request ?

If you have any feature request, feel free to open an issue on the [GitHub repository](https://github.com/cybermaxs/github-stars-monitor/issues).

## Credits

This project is heavily inspired by [mdsinabox](https://github.com/matsonj/nba-monte-carlo) and [pypi-duck-flow](https://github.com/mehd-io/pypi-duck-flow).
