select
    year,
    team,
    sum(points) as total_points
from {{ ref('fct_results') }}
group by year, team
order by year, total_points desc