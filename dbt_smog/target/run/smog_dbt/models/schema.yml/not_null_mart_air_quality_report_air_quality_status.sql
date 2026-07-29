
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select air_quality_status
from `de-project-001-503509`.`smog_warehouse`.`mart_air_quality_report`
where air_quality_status is null



  
  
      
    ) dbt_internal_test