with stars as (
    select repository, cumulative_stars from {{ ref('stars') }}
    qualify row_number() over (partition by repository order by day desc) = 1
)

select * from {{ ref('repositories') }}
inner join stars
on repositories.repository = stars.repository
where abs(stars.cumulative_stars - repositories.stargazers_count) / repositories.stargazers_count > 0.01
