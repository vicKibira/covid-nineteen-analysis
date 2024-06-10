{{
    config(materialized='view',
    post_hooks="
    create materialized view if not exists {{this.schema}}.mv_stg_one_week_increase as 
    select
        rn,
        one_week_increase
    from {{ref('stg_covid_data)}}
    create index if not exists idx_one_week_increase on {{this.schema}}.mv_stg_one_week_increase('one_week_increase)
    ")
}}
select
   *
from {{ref('stg_covid_data')}}