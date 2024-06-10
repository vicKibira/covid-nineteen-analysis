{{
    config(materialized='view',
    post_hooks="
    create materialized view if not exists {{this.schema}}.mv_stg_one_week_change as 
    select
        rn,
        one_week_change
    from {{ref('stg_covid_data')}}
    group by one_week_change,rn
    
    create index if not exists idx_one_week_change on {{this.schema}}.mv_stg_one_week_change(one_week_change)
    "
    )
}}
select
    *
from {{ref('stg_covid_data')}}