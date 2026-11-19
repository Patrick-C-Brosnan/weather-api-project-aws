select *
from {{ ref('int_weather_forecast_hours') }}
where min_temperature is NULL 
or max_temperature is NULL
or min_wind_speed is NULL
or max_wind_speed is NULL