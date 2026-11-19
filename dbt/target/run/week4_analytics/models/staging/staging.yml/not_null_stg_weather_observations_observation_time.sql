
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select observation_time
from "analytics"."dbt_patrick"."stg_weather_observations"
where observation_time is null



  
  
      
    ) dbt_internal_test