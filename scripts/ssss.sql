select * from dim_new_cases

	
select 
	  sum(total_new_cases) as total_new_cases
from dim_new_cases

select * from dim_new_recovered

select
	  sum(total_new_recovered) as total_new_recovered
from dim_new_recovered

select * from dim_confirmed
	
select * from dim_country

select
	 c.country as country,
	 p.total_cases_confirmed as total_cases_confirmed	 
from dim_confirmed p
left join dim_country c on p.rn = c.rn
group by country,total_cases_confirmed
order by total_cases_confirmed desc


select
	 c.country as country ,
	 p.total_cases_confirmed as total_cases_confirmed	
from dim_country c
left join dim_confirmed p on c.rn=p.rn
group by country,total_cases_confirmed

select 
	--c.country as country,
	w.who_region as who_region,
	sum(d.total_cases_confirmed) as total_cases_confirmed
from dim_who_region w
--left join dim_country c on w.rn = c.rn
left join dim_confirmed d on w.rn = d.rn
where who_region = 'Europe'
group by who_region,total_cases_confirmed

SELECT 
    SUM(d.total_cases_confirmed) as total_cases_confirmed
FROM dim_who_region w
--LEFT JOIN dim_country c ON w.rn = c.rn
LEFT JOIN dim_confirmed d ON w.rn = d.rn
WHERE who_region = 'Europe';
