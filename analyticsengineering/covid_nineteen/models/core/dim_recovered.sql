{{
    config(materialized='view')
}}
with stg_recovered as (
    select
        rn,
        recovered
    from {{ref('mv_stg_recovered')}}
  
)
select
   rn,
   sum(recovered) as totally_recovered
from stg_recovered
group by rn,recovered