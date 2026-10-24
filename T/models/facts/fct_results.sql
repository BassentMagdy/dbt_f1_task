select
    r.race_url,
    ra.year,
    ra.grand_prix,
    r.first_name,
    r.last_name,
    r.team,
    r.position,
    r.points
from {{ ref('stg_results') }} r
join {{ ref('dim_races') }} ra
    on r.race_url = ra.race_url