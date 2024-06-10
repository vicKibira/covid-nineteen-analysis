{{
    config(materialized='view',
    post_hooks="
    create materialized view if not exists {{this.schema}}.mv_stg_new_recovered as
    select
        rn,
        new_recovered
    from {{ref('stg_covid_data)}}
    group by new_recovered, rn

    create index if not exists idx_total_new_recovered on {{this.schema}}.mv_stg_new_recovered(new_recovered)

    "
    )
}}
select
   *
from {{ref('stg_covid_data')}}