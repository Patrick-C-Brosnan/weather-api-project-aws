select
    location_id,
    observation_time,
    count(*) as row_count
from {{ ref('stg_weather_observations') }}
group by
    location_id,
    observation_time
having count(*) > 1