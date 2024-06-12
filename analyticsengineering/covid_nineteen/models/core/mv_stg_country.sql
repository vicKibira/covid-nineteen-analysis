{{
    config(materialized='view',
    post_hooks="
    create materialized view if not exists {{this.schema}}.mv_stg_country as 
    select
        rn,
        country
    from {{ref('stg_covid_data')}}
    group by rn
    create index if not exists idx_country on {{this.schema}}.mv_stg_country(country)
    " 
    )
}}
select
  *
from {{ref('stg_covid_data')}}