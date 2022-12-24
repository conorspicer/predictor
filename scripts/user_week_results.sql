create or replace view user_week_results as 
(select id as user, all_user_weeks.week, COALESCE(user_points, 0) as user_points
from 
(select * from 
	(select distinct id from auth_user) users 
	cross join 
	(select distinct `week` from fixtures_fixture) weeks
) all_user_weeks
left join (
	select user, week, sum(user_points) as user_points
	from user_scores
	where changeable = 1
	group by user, week
) a on all_user_weeks.id=a.user and all_user_weeks.week=a.week
UNION ALL (VALUES 
	ROW(11, 23, 0 ),
	ROW(12, 23, 0),
	ROW(13, 23, 0),
    ROW(14, 23, 0)
));