select
    repository
    , date_trunc('day', starred_at) as day
    , count(distinct user_login) as stars
from {{ ref('stg_stargazers') }}
inner join {{ ref('stg_repositories') }} using (repository)
group by repository, day
