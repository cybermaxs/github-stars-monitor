WITH source_data AS (
    SELECT * FROM {{ source('raw', 'repositories') }}
)

SELECT
    id
    , lower(full_name) as repository
    , html_url
    , created_at
    , updated_at
    , pushed_at
    , homepage
    , stargazers_count
    , forks_count
    , watchers_count
    , open_issues_count
    , language
FROM source_data
