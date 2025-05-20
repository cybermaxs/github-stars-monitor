---
title: Trending recently created repositories
---

Display the most starred repositories (> 500 stars) created in the last 2 months.
Data is updated daily.

```sql metrics
  select
      count(distinct repository) as repository_count
      , sum(cumulative_stars) as cumulative_stars
  from github.stars
```

```sql last_refresh_at
select last_inserted_at from github.dlt
```

## Indexed repositories

<BigValue
    title='Total Repositories'
    data={metrics}
    value='repository_count'
/>

<BigValue
    title='Total Stars'
    data={metrics}
    value='cumulative_stars'
    fmt='#,##0.00,"k"'
/>

<BigValue
  title='Data last updated on'
  data={last_refresh_at}
  value=last_inserted_at
/>

## Most starred repositories

```sql languages
    select
        language
    from
        github.repositories
```

```sql repositories
with daily_stars as (
    select
        repository,
        day,
        stars
    from
        github.stars
)
, aggregated_stars as (
    select
        repository,
        ARRAY_AGG({'date': day, 'stars': stars}) AS stars
    from daily_stars
    group by repository
)

select
    rep.repository
    , rep.created_at
    , rep.stargazers_count
    , rep.forks_count
    , rep.open_issues_count
    , rep.html_url
    , rep.language
    , rep.stars_1d / rep.stargazers_count as stars_1d_ratio
    , CASE WHEN rep.created_at < CURRENT_DATE - INTERVAL '3 days' THEN rep.stars_3d / rep.stargazers_count ELSE null END as stars_3d_ratio
    , CASE WHEN rep.created_at < CURRENT_DATE - INTERVAL '7 days' THEN rep.stars_7d / rep.stargazers_count ELSE null END as stars_7d_ratio
    , CASE WHEN rep.created_at < CURRENT_DATE - INTERVAL '30 days' THEN rep.stars_30d / rep.stargazers_count ELSE null END as stars_30d_ratio
    , aggregated_stars.stars
from github.repositories as rep
inner join aggregated_stars on rep.repository = aggregated_stars.repository
where rep.language in ${inputs.language.value}
```

```sql stars
select *
from github.stars
```

<Dropdown
    title="Filter by language"
    data={languages}
    name=language
    label=language
    value=language
    multiple=true
    selectAllByDefault=true
/>

<DataTable data={repositories} search=true sort="stargazers_count desc" rows=20 emptyMessage="No repositories found">
    <Column id=html_url contentType=link linkLabel=repository openInNewTab=true />
    <Column id=language />
    <Column id=created_at title="Created" />
    <Column id=stargazers_count title="Stars" />
    <Column id=stars title="Trend" contentType=sparkline sparkX=date sparkY=stars />
    <Column id=stars_1d_ratio fmt=pct1 title="Growth 1D" contentType=colorscale colorScale=positive/>
    <Column id=stars_3d_ratio fmt=pct1 title="Growth 2D" contentType=colorscale colorScale=positive/>
    <Column id=stars_7d_ratio fmt=pct1 title="Growth 7D" contentType=colorscale colorScale=positive/>
    <Column id=stars_30d_ratio fmt=pct1 title="Growth 30D" contentType=colorscale colorScale=positive/>
</DataTable>


## Most starred repositories since {inputs.range} day(s)

```sql most_starred_list
select repository, sum(stars) as stars
    from github.stars
    where day >= CURRENT_DATE - INTERVAL '${inputs.range}' day
    group by repository
    order by sum(stars) desc
    limit 10
```

<ButtonGroup
    name=range >
    <ButtonGroupItem valueLabel="Last day" value="1" />
    <ButtonGroupItem valueLabel="Last Week" value="7" default />
    <ButtonGroupItem valueLabel="Last Month" value="30" />
</ButtonGroup>

<BarChart
    data={most_starred_list}
    x=repository
    y=stars
    swapXY=true
/>

## Individual repository graph

```sql repositories_list
  select
    repository
  from github.repositories
```

```sql most_starred
select repository, day, stars, cumulative_stars
from github.stars
where repository = '${inputs.dd_repository.value}'
```

<Dropdown
    title="Select a Repository"
    data={repositories_list}
    name=dd_repository
    label=repository
    value=repository
/>

<LineChart
    data={most_starred}
    x=day
    y2=stars
    y2AxisTitle="Daily stars"
    series=repository
    y=cumulative_stars
    yAxisTitle="Cumulative stars"
    y2SeriesType=bar
/>


*Made by [Maxime Lemaitre](https://www.linkedin.com/in/maxime-lemaitre-data/)*
