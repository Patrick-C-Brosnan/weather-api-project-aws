
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select fetched_at
from "analytics"."dbt_patrick"."stg_weather_observations"
where fetched_at is null



  
  
      
    ) dbt_internal_test