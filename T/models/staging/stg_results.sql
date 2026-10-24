select
    url as race_url,
    pos as position,
    driver_first_name as first_name,
    driver_last_name as last_name,
    driver_short_name as short_name,
    team,
    laps,
    time_retired,
    cast(pts as numeric) as points
from {{ source('raw', 'raw_results') }}