 {{
    config(materialized='view')
 }}

 with stg_one_week_change as (
    select
         rn,
         one_week_change
    from {{ref('mv_stg_one_week_change')}}
 )
 select
    *
 from stg_one_week_change
 group by rn,one_week_change