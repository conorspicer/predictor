CREATE OR REPLACE VIEW user_totals AS (
	select user, sum(user_points) as user_points
	from user_scores
	where changeable = 1
    group by user
) 