{{
    config(materialized='view')
}}
with stg_one_week_increase as (
    select
       rn,
       one_week_increase
    from{{ref('mv_stg_one_week_increase')}}
)
select 
   *
from stg_one_week_increase
group by rn, one_week_increase