{{
    config(materialized='view')
}}

with stg_confirmed_last_week as (
    select
         rn,
         confirmed_last_week
    from {{ref('mv_stg_confirmed_last_week')}}
)
select
    *
from stg_confirmed_last_week
group by rn,confirmed_last_week