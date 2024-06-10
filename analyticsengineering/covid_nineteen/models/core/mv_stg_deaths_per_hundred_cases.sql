{{
    config(materialized='view',
    post_hooks="
    create materialized view if not exists {{this.schema}}.mv_deaths_per_hundred_cases as 
    select
        rn,
        deaths_per_hundred_cases
    from {{ref('stg_covid_data')}}
    group by deaths_per_hundred_cases,rn
    
    create index if not exists  idx_total_deaths_per_hundred_cases on {{this.schema}}.mv_deaths_per_hundred_cases(deaths_per_hundred_cases)

    ")
}}
select
    *
from {{ref('stg_covid_data')}}