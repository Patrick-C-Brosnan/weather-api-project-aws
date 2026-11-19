
  create view "analytics"."dbt_patrick"."int_weather_forecast_hours__dbt_tmp"
    
    
  as (
    with forecasts as (

    select *
    from "analytics"."dbt_patrick"."stg_weather_observations"

)

select location_id,
       extract(DAY from observation_time) as observation_day,
       count(*) as hourly_predictions,
       min(temperature_c) as min_temperature,
       max(temperature_c) as max_temperature,
       min(wind_speed_kph) as min_wind_speed,
       max(wind_speed_kph) as max_wind_speed
from forecasts
group by 1,2
order by 1,2
  );