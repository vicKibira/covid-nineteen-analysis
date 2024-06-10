{{
    config(materialized='view',
    post_hooks="
    create materialized view if not exists {{this.schema}}.mv_stg_new_cases as 
    select
        rn,
        new_cases
    from {{ref('stg_covid_data')}}
    group by new_cases,rn

    create index if not exists idf_total_new_cases on {{this.schema}}.mv_stg_new_cases(new_cases)
    "
    )
}}
select
 *
from {{ref('stg_covid_data')}}