
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select *
from "analytics"."dbt_patrick"."int_weather_forecast_hours"
where min_temperature is NULL 
or max_temperature is NULL
or min_wind_speed is NULL
or max_wind_speed is NULL
  
  
      
    ) dbt_internal_test