{{
    config(materialized='view',
    post_hooks="
    create materialized view if not exists {{this.schema}}.mv_stg_recovered as
    select
       rn,
       recovered
    from {{ref('stg_covid_data')}}
    group by recovered, rn

    create index if not exists idx_total_recovered on {{this.schema}}.mv_stg_recovered(recovered) 
    "  
    )
}}
select
   *
from {{ref('stg_covid_data')}}