{{
    config(materialized='view',
    post_hooks="
    create materialized view if not exists {{this.schema}}.mv_stg_confirmed_last_week as 
    
    select
        rn,
        confirmed_last_week
    from {{ref('stg_covid_data')}}
    group by confirmed_last_week, rn

    create index if not exists idx_confirmed_last_week on {{this.schema}}.mv_stg_confirmed_last_week(confirmed_last_week)
    
    ")
}}

select
     rn,
     confirmed_last_week
from {{ref('stg_covid_data')}}