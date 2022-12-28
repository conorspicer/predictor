-- create or replace view user_week_results as (

select 
	a.user_id as user, 
    a.week, 
    CASE
		WHEN a.week=23 and a.user_id=11 THEN 0   -- conorspicer
        WHEN a.week=23 and a.user_id=12 THEN 0   -- torinmehmet
        WHEN a.week=23 and a.user_id=13 THEN 0   -- magnusmartinsen
        WHEN a.week=23 and a.user_id=14 THEN 0   -- lewismead
        ELSE COALESCE(user_points, 0) 
	END as user_points
from 
results_userweekresult a
left join (
	select user, week, sum(user_points) as user_points
	from user_scores
	where changeable = 1
	group by user, week
) b on a.user_id=b.user and a.week=b.week

-- );