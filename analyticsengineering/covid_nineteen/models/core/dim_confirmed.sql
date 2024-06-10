{{
    config(materialized='view')
}}

with stg_confirmed as (
    select
       rn,
       confirmed
    from {{ref('mv_stg_confirmed')}}
)
select
   rn,
   sum(confirmed) as total_cases_confirmed
from stg_confirmed
group by rn