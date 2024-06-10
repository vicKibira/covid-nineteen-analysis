{{
    config(materialized='view')
}}
with stg_recovered_per_hundred_cases as(
    select
        rn,
        recovered_per_hundred_cases
    from {{ref('mv_stg_recovered_per_hundred_cases')}}
)
select
     rn,
     recovered_per_hundred_cases
from stg_recovered_per_hundred_cases
group by rn, recovered_per_hundred_cases