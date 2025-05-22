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
    , coalesce(language, '(Unknown)') as language
FROM source_data
