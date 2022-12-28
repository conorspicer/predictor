UPDATE  picks_pick p
-- select * from picks_pick p
left join fixtures_fixture f on p.fixture_id=f.id
left join auth_user u on p.user_id=u.id
SET p.home_pick = 30, p.away_pick = 20
WHERE u.username IN ('magnusmartinsen')
	AND f.week = 16
	AND f.ko_datetime > '2022-09-01'  # 2022 season
 	-- AND f.ko_datetime < '2022-12-24'  # TNF only
