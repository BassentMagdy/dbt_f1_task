select
    year,
    driver_first_name as first_name,
    driver_last_name as last_name,
    driver_nationality as nationality,
    team,
    cast(pts as numeric) as points
from {{ source('raw', 'raw_drivers') }}