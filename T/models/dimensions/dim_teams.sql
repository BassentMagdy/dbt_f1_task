select distinct
    team as team_name
from {{ ref('stg_results') }}