
  create view "analytics"."dbt_patrick"."stg_weather_observations__dbt_tmp"
    
    
  as (
    

select
    location_id,
    location_name,
    latitude,
    longitude,
    observation_time,
    temperature_c,
    precipitation_mm,
    wind_speed_kph,
    relative_humidity_pct,
    fetched_at
from "analytics"."weather_raw"."raw_weather_observations"
  );