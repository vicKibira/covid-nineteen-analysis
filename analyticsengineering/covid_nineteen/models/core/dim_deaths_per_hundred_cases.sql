{{
    config(materialized='view')
}}
with stg_deaths_per_hundred_cases as (
    select
       rn,
       deaths_per_hundred_cases
    from {{ref('mv_stg_deaths_per_hundred_cases')}}
)
select
      rn,
      deaths_per_hundred_cases
   -- sum(deaths_per_hundred_cases) as total_deaths_per_hundred_cases
from stg_deaths_per_hundred_cases
group by  rn,deaths_per_hundred_cases