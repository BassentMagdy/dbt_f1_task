select distinct
    first_name,
    last_name,
    short_name
from {{ ref('stg_results') }}