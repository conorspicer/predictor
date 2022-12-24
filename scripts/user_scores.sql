CREATE OR REPLACE VIEW user_scores AS (
SELECT points.*,
       ((`points`.`winner_pts` + `points`.`margin_pts`) + `points`.`total_score_pts`) AS `user_points`
FROM (
       SELECT predictions.*, 
              CASE
                     WHEN (`predictions`.`user_winner` = `predictions`.`actual_winner`) and `predictions`.`ko_datetime` < CURRENT_TIMESTAMP()
                     THEN 25
                     ELSE 0
              END AS `winner_pts`,
              CASE
                     WHEN ((10 - abs((COALESCE(`predictions`.`user_margin`,0) - COALESCE(`predictions`.`actual_margin`,0)))) > 0) and `predictions`.`ko_datetime` < CURRENT_TIMESTAMP()
                     THEN (10 - abs((COALESCE(`predictions`.`user_margin`,0) - COALESCE(`predictions`.`actual_margin`,0))))
                     ELSE 0
              END AS `margin_pts`,
              CASE
                     WHEN ((10 - abs((COALESCE(`predictions`.`user_total_score`,0) - COALESCE(`predictions`.`actual_total_score`,0)))) > 0) and `predictions`.`ko_datetime` < CURRENT_TIMESTAMP()
                     THEN (10 - abs((COALESCE(`predictions`.`user_total_score`,0) - COALESCE(`predictions`.`actual_total_score`,0))))
                     ELSE 0
              END AS `total_score_pts`
       FROM(       
              SELECT raw_picks.*,
                     abs((COALESCE(`raw_picks`.`home_pick`,0) - COALESCE(`raw_picks`.`away_pick`,0))) AS `user_margin`,
                     (`raw_picks`.`home_pick` + `raw_picks`.`away_pick`)                              AS `user_total_score`,
                     CASE
                            WHEN (`raw_picks`.`home_pick` > `raw_picks`.`away_pick`) 
                                THEN `raw_picks`.`home_team_name`
                            WHEN (`raw_picks`.`away_pick` > `raw_picks`.`home_pick`) 
                                THEN `raw_picks`.`away_team_name`
                            ELSE 'TIE'
                     END                                                                                                AS `user_winner`,
                     abs((COALESCE(`raw_picks`.`home_score`,0) - COALESCE(`raw_picks`.`away_score`,0))) AS `actual_margin`,
					`raw_picks`.`home_score` + `raw_picks`.`away_score`                                 AS `actual_total_score`,
                     CASE
                            WHEN isnull(`raw_picks`.`home_score`) OR isnull(`raw_picks`.`away_score`) THEN 'NULL'
                            WHEN (`raw_picks`.`home_score` > `raw_picks`.`away_score`) THEN `raw_picks`.`home_team_name`
                            WHEN (`raw_picks`.`away_score` > `raw_picks`.`home_score`) THEN `raw_picks`.`away_team_name`
                            ELSE 'TIE'
                     END AS `actual_winner`
              FROM (
                     SELECT   `p`.`id`            AS `pick_id`,
                              `f`.`ko_datetime`   AS `ko_datetime`,
                              case when `p`.`home_pick` is null then 30 else `p`.`home_pick` END AS `home_pick`,
                              case when `p`.`away_pick` is null then 20 else `p`.`away_pick` END AS `away_pick`,
                              `p`.`lock`          AS `locked`,
                              `f`.`away_score`,
                              `f`.`home_score`,
                              `f`.`week`          AS `week`,
                              `f`.`changeable`    AS `changeable`,
                              `u`.`id`            AS `user`,
                              `away`.`team_name`  AS `away_team_name`,
                              `home`.`team_name`  AS `home_team_name`
                     FROM `picks_pick` `p`
                     LEFT JOIN  `fixtures_fixture` `f`
                       ON `p`.`fixture_id` = `f`.`id`
                     JOIN     `auth_user` `u`
                       ON `u`.`id` = `p`.`user_id`
                     LEFT JOIN     `fixtures_team` `away`
                       ON `away`.`id` = `f`.`away_team_id`
                     LEFT JOIN     `fixtures_team` `home`
                       ON `home`.`id` = `f`.`home_team_id`
                     ) raw_picks
       ) predictions
) points 
);
