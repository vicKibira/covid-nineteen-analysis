{{
    config(materialized='view')
}}

with stg_deaths as (
    select
        rn,
        deaths
    from {{ref('mv_stg_deaths')}}
)
select
   rn,
   sum(deaths) as total_deaths
from stg_deaths
group by rn