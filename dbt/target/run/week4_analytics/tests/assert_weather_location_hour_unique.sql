
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select
    location_id,
    observation_time,
    count(*) as row_count
from "analytics"."dbt_patrick"."stg_weather_observations"
group by
    location_id,
    observation_time
having count(*) > 1
  
  
      
    ) dbt_internal_test