select
    repository
    , date_trunc('day', starred_at) as day
    , count(distinct user_login) as stars
from {{ ref('stg_stargazers') }}
group by repository, day
