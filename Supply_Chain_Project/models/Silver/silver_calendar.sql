select date,year,quarter,month,day,week,day_of_week from {{ ref('brz_calendar') }}

WHERE date IS not NULL;