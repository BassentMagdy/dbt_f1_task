select distinct
    year,
    grand_prix,
    url as race_url,
    date as race_date,
    winner_driver_first_name,
    winner_driver_last_name,
    winner_team
from {{ source('raw', 'raw_races') }}