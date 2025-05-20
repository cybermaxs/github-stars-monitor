
select
    rep.*
    , agg.* exclude (repository)
from {{ ref('stg_repositories') }} as rep
inner join {{ ref('repositories_aggregated')}} as agg
    on rep.repository = agg.repository
