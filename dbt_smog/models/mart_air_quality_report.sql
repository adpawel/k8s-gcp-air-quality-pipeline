with source as (
    select * from {{ source('raw_data', 'krakow_air_quality') }}
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
            when european_aqi <= 20 then '🟢 Bardzo dobra'
            when european_aqi <= 40 then '🟢 Dobra'
            when european_aqi <= 60 then '🟡 Umiarkowana'
            when european_aqi <= 80 then '🟠 Zła'
            else '🔴 Bardzo zła'
        end as air_quality_status,
        source_file,
        current_timestamp() as dbt_updated_at
    from source
)

select * from transformed
order by measurement_timestamp desc