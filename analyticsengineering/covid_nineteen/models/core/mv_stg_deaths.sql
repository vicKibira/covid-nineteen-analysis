{{
    config(materialized='view',
           post_hooks="
           create materialized view if not exists {{this.schema}}.mv_stg_deaths as
           select
               rn,
               deaths
           from {{ref('stg_covid_data)}}
           group by deaths, rn
           
           create index if not exists idx_total_deaths on {{this.schema}}.mv_stg_deaths(deaths)
           "
    )
}}
select
   *
from {{ref('stg_covid_data')}}