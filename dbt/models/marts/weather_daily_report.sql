with daily_forecasts as (

    select *
    from {{ ref('int_forecast_daily_summary') }}

)

select
    location_id,
    observation_date,
    hourly_predictions,

    min_temperature as min_temperature_c,
    max_temperature as max_temperature_c,
    max_temperature - min_temperature as temperature_range_c,

    min_wind_speed as min_wind_speed_kph,
    max_wind_speed as max_wind_speed_kph,

    dense_rank() over (
        partition by observation_date
        order by max_temperature desc nulls last
    ) as temperature_rank

from daily_forecasts