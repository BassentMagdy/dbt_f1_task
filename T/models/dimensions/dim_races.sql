select
    race_url,
    year,
    grand_prix,
    race_date
from {{ ref('stg_races') }}