
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select measurement_timestamp
from `de-project-001-503509`.`smog_warehouse`.`mart_air_quality_report`
where measurement_timestamp is null



  
  
      
    ) dbt_internal_test