{{
    config(
        materialized='view',
        post_hooks="
        create materialized view if not exists {{this.schema}}.mv_stg_confirmed as 
        select
            rn,
            confirmed
        from {{ref('stg_covid_data')}}
        
        create index if not exists idx_total_cases on {{this.schema}}.mv_stg_confirmed(confirmed)
        
        "
        )
}}
select
   *
from {{ref('stg_covid_data')}}