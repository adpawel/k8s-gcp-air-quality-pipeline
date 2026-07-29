
  
    

    create or replace table `de-project-001-503509`.`smog_warehouse`.`mart_air_quality_report`
      
    
    

    
    OPTIONS()
    as (
      with source as (
    select * from `de-project-001-503509`.`smog_warehouse`.`krakow_air_quality`
    qualify row_number() over (partition by timestamp order by source_file desc) = 1
),

transformed as (
    select
        timestamp(timestamp) as measurement_timestamp,
        format_timestamp('%Y-%m-%d %H:%M', timestamp(timestamp)) as formatted_time,
        city,
        pm10,
        pm2_5,
        european_aqi,
        case 
            when european_aqi <= 20 then 'Bardzo dobra'
            when european_aqi <= 40 then 'Dobra'
            when european_aqi <= 60 then 'Umiarkowana'
            when european_aqi <= 80 then 'Zla'
            else 'Bardzo zla'
        end as air_quality_status,
        source_file,
        current_timestamp() as dbt_updated_at
    from source
)

select * from transformed
order by measurement_timestamp desc
    );
  