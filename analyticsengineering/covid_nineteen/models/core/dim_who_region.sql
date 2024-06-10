{{
    config(materialized='view')
}}
with stg_who_region as (
    select
        rn,
        who_region
    from {{ref('mv_stg_who_region')}}
)
select
    *
from stg_who_region