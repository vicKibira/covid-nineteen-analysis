{{
    config(materialized='view')
}}
with stg_country as (
    select
        rn,
        country
    from {{ref('mv_stg_country')}}
)
select
*
from stg_country
group by rn,country