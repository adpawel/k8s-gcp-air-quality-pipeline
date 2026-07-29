
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        air_quality_status as value_field,
        count(*) as n_records

    from `de-project-001-503509`.`smog_warehouse`.`mart_air_quality_report`
    group by air_quality_status

)

select *
from all_values
where value_field not in (
    'Bardzo dobra','Dobra','Umiarkowana','Zła','Bardzo zła'
)



  
  
      
    ) dbt_internal_test