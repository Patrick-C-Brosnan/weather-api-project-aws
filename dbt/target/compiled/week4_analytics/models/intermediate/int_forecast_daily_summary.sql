with forecasts as (

    select *
    from "analytics"."dbt_patrick"."stg_weather_observations"

)

select
    location_id,
    (observation_time at time zone 'Europe/London')::date as observation_date,
    count(*) as hourly_predictions,
    min(temperature_c) as min_temperature,
    max(temperature_c) as max_temperature,
    min(wind_speed_kph) as min_wind_speed,
    max(wind_speed_kph) as max_wind_speed
from forecasts
group by 1, 2