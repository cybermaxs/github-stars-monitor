WITH source_data AS (
    SELECT * FROM {{ source('raw', 'stargazers') }}
)

SELECT
    user__login as user_login
    , starred_at
    , lower(repository_full_name) as repository
FROM source_data
