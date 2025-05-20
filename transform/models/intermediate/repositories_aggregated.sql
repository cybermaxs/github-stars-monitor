with stars as (
    select
          repository
        , starred_at::date as starred_date
        , user_login
    from {{ ref('stg_stargazers') }}
)
, agg as (
    select
          s.repository
        , count(distinct case when starred_date >= current_date - interval '1 day' then user_login end) as stars_1d
        , count(distinct case when starred_date >= current_date - interval '3 day' then user_login end) as stars_3d
        , count(distinct case when starred_date >= current_date - interval '7 day' then user_login end) as stars_7d
        , count(distinct case when starred_date >= current_date - interval '30 day' then user_login end) as stars_30d
        , count(distinct case when starred_date >= current_date - interval '60 day' then user_login end) as stars_60d
    from stars s
    group by s.repository
)
select
      repository
    , stars_1d
    , stars_3d
    , stars_7d
    , stars_30d
    , stars_60d
from agg
