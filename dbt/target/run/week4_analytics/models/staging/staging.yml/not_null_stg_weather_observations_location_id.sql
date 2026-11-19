
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select location_id
from "analytics"."dbt_patrick"."stg_weather_observations"
where location_id is null



  
  
      
    ) dbt_internal_test