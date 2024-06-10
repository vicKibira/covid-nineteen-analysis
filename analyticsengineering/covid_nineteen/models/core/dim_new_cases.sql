{{
    config(materialized='view')
}}
with stg_new_cases as (
    select
       rn,
       new_cases
    from {{ref('mv_stg_new_cases')}}

)
select
   rn,
   sum(new_cases) as total_new_cases
from stg_new_cases
group by rn
