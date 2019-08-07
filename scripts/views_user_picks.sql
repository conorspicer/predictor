CREATE
OR REPLACE VIEW ALL_USER_RAW_PICKS AS
SELECT
  f.ko_datetime AS ko_datetime,
  p.home_pick AS home_pick,
  p.away_pick AS away_pick,
  p.lock AS lock,
  f.away_score AS away_score,
  f.home_score AS home_score,
  f.week AS week,
  u.username AS username,
  away.team_name AS away_team_name,
  away.division AS away_division,
  away.conference AS away_conference,
  home.team_name AS home_team_name,
  home.division AS home_division,
  home.conference AS home_conference
FROM
  (
    (
      (
        (
          picks_pick p
          JOIN fixtures_fixture f ON ((p.fixture_id = f.id))
        )
        JOIN auth_user u ON ((u.id = p.user_id))
      )
      JOIN fixtures_team away ON ((away.id = f.away_team_id))
    )
    JOIN fixtures_team home ON ((home.id = f.home_team_id))
  )
ORDER BY
  f.ko_datetime;

CREATE OR REPLACE VIEW `ALL_USER_PREDICTIONS` AS
SELECT
  *,
  abs(COALESCE(home_pick, 0) - COALESCE(away_pick, 0)) as user_margin,
  home_pick + away_pick as user_total_score,
  CASE
    WHEN home_pick > away_pick THEN 'HOME'
    WHEN away_pick > home_pick THEN 'AWAY'
    ELSE 'TIE'
  END as 'user_winner',
  abs(
    COALESCE(home_score, 0) - COALESCE(away_score, 0)
  ) as actual_margin,
  home_score + away_score as actual_total_score,
  CASE
    WHEN home_score IS NULL THEN 'NULL'
    WHEN away_score IS NULL THEN 'NULL'
    WHEN home_score > away_score THEN 'HOME'
    WHEN away_score > home_score THEN 'AWAY'
    ELSE 'TIE'
  END as 'actual_winner'
FROM
  ALL_USER_RAW_PICKS;


CREATE OR REPLACE VIEW `ALL_USER_PICKS` AS
SELECT
  *,
  CASE
    WHEN user_winner = actual_winner THEN 25
    ELSE 0
  END as 'winner_pts',
  CASE
    WHEN 10 - ABS(
      COALESCE(user_margin, 0) - COALESCE(actual_margin, 0)
    ) > 0 THEN 10 - ABS(
      COALESCE(user_margin, 0) - COALESCE(actual_margin, 0)
    )
    ELSE 0
  END as 'margin_pts',
  CASE
    WHEN 10 - ABS(
      COALESCE(user_total_score, 0) - COALESCE(actual_total_score, 0)
    ) > 0 THEN 10 - ABS(
      COALESCE(user_total_score, 0) - COALESCE(actual_total_score, 0)
    )
    ELSE 0
  END as 'total_score_pts'

FROM
  ALL_USER_PREDICTIONS;

CREATE OR REPLACE VIEW `ALL_USER_POINTS` AS
SELECT
  *,
  'winner_pts' + 'margin_pts' + 'total_score_pts' as 'points'
  
FROM
  ALL_USER_PICKS;


SELECT * FROM ALL_USER_POINTS;
