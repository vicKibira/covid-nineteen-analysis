{{
    config(materialized='view',
    post_hooks="
    create materialized view if not exists {{this.schema}}.mv_stg_covered_per_hundred_cases as
    select
        rn,
        recovered_per_hundred_cases
    from {{ref('stg_covid_data')}}
    group by recovered_per_hundred_cases,rn

    create index if not exists idx_total_recovered_per_hundred_cases on {{this.schema}}.mv_stg_covered_per_hundred_cases(recovered_per_hundred_cases)
    ")
}}
select
 *
from{{ref('stg_covid_data')}}