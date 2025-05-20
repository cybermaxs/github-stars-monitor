select
  repository,
  day,
  stars,
  sum(stars) over (
    partition by repository
    order by day
    rows between unbounded preceding and current row
  ) as cumulative_stars
from {{ ref('stargazers_daily') }}
order by repository, day
