{{
    config(materialized='view',
    post_hooks="
    create materialized view if not exists {{this.schema}}.mv_stg_who_region as
    select
       rn,
       who_region
    from{{ref('stg_covid_data')}}
    group by who_region
    
    create index if not exists idx_who_region on {{this.schema}}.mv_stg_who_region(who_region)
    ")
}}
select
*
from {{ref('stg_covid_data')}}