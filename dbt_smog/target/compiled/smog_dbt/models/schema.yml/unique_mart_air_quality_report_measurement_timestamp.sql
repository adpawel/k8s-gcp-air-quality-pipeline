
    
    

with dbt_test__target as (

  select measurement_timestamp as unique_field
  from `de-project-001-503509`.`smog_warehouse`.`mart_air_quality_report`
  where measurement_timestamp is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


