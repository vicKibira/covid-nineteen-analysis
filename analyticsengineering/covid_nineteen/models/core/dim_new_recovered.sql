{{
    config(materialized='view')
}}
with stg_new_recovered as (
    select
        rn,
        new_recovered
    from {{ref('mv_stg_new_recovered')}}
)
select
   rn,
   sum(new_recovered) as total_new_recovered
from stg_new_recovered
group by rn,new_recovered