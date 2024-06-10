{{
    config(materialized='view')
}}

with stg_covid_data as (
    select
        row_number() over() as rn,
       "index" as index,
       "Country/Region" as country,
       "Confirmed" as confirmed,
       "Deaths" as deaths,
       "Recovered" as recovered,
       "Active" as active,
       "New cases" as new_cases,
       "New recovered" as new_recovered,
       "Deaths / 100 Cases" as deaths_per_hundred_cases,
       "Recovered / 100 Cases" as recovered_per_hundred_cases,
       "Deaths / 100 Recovered" as deaths_per_hundred_recovered,
       "Confirmed last week" as confirmed_last_week,
       "1 week change" as one_week_change,
       "1 week % increase" as one_week_increase,
       "WHO Region" as who_region
    from{{source('covid','covid_datatable')}}
)
select
   *
from stg_covid_data