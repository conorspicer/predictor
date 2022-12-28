create or replace view `user_scores` AS
    (SELECT
        `points`.`pick_id` AS `pick_id`,
        `points`.`ko_datetime` AS `ko_datetime`,
        `points`.`home_pick` AS `home_pick`,
        `points`.`away_pick` AS `away_pick`,
        `points`.`locked` AS `locked`,
        `points`.`away_score` AS `away_score`,
        `points`.`home_score` AS `home_score`,
        `points`.`week` AS `week`,
        `points`.`changeable` AS `changeable`,
        `points`.`user` AS `user`,
        `points`.`away_team_name` AS `away_team_name`,
        `points`.`home_team_name` AS `home_team_name`,
        `points`.`user_margin` AS `user_margin`,
        `points`.`user_total_score` AS `user_total_score`,
        `points`.`user_winner` AS `user_winner`,
        `points`.`actual_margin` AS `actual_margin`,
        `points`.`actual_total_score` AS `actual_total_score`,
        `points`.`actual_winner` AS `actual_winner`,
        `points`.`winner_pts` AS `winner_pts`,
        `points`.`margin_pts` AS `margin_pts`,
        `points`.`total_score_pts` AS `total_score_pts`,
        ((`points`.`winner_pts` + `points`.`margin_pts`) + `points`.`total_score_pts`) AS `user_points`
    FROM
        (SELECT
            `predictions`.`pick_id` AS `pick_id`,
                `predictions`.`ko_datetime` AS `ko_datetime`,
                `predictions`.`home_pick` AS `home_pick`,
                `predictions`.`away_pick` AS `away_pick`,
                `predictions`.`locked` AS `locked`,
                `predictions`.`away_score` AS `away_score`,
                `predictions`.`home_score` AS `home_score`,
                `predictions`.`week` AS `week`,
                `predictions`.`changeable` AS `changeable`,
                `predictions`.`user` AS `user`,
                `predictions`.`away_team_name` AS `away_team_name`,
                `predictions`.`home_team_name` AS `home_team_name`,
                `predictions`.`user_margin` AS `user_margin`,
                `predictions`.`user_total_score` AS `user_total_score`,
                `predictions`.`user_winner` AS `user_winner`,
                `predictions`.`actual_margin` AS `actual_margin`,
                `predictions`.`actual_total_score` AS `actual_total_score`,
                `predictions`.`actual_winner` AS `actual_winner`,
                (CASE
                    WHEN
                        ((`predictions`.`user_winner` = `predictions`.`actual_winner`)
                            AND (`predictions`.`ko_datetime` < NOW()))
                    THEN
                        25
                    ELSE 0
                END) AS `winner_pts`,
                (CASE
                    WHEN
                        (((10 - ABS((COALESCE(`predictions`.`user_margin`, 0) - COALESCE(`predictions`.`actual_margin`, 0)))) > 0)
                            AND (`predictions`.`ko_datetime` < NOW()))
                    THEN
                        (10 - ABS((COALESCE(`predictions`.`user_margin`, 0) - COALESCE(`predictions`.`actual_margin`, 0))))
                    ELSE 0
                END) AS `margin_pts`,
                (CASE
                    WHEN
                        (((10 - ABS((COALESCE(`predictions`.`user_total_score`, 0) - COALESCE(`predictions`.`actual_total_score`, 0)))) > 0)
                            AND (`predictions`.`ko_datetime` < NOW()))
                    THEN
                        (10 - ABS((COALESCE(`predictions`.`user_total_score`, 0) - COALESCE(`predictions`.`actual_total_score`, 0))))
                    ELSE 0
                END) AS `total_score_pts`
        FROM
            (SELECT
            `raw_picks`.`pick_id` AS `pick_id`,
                `raw_picks`.`ko_datetime` AS `ko_datetime`,
                `raw_picks`.`home_pick` AS `home_pick`,
                `raw_picks`.`away_pick` AS `away_pick`,
                `raw_picks`.`locked` AS `locked`,
                `raw_picks`.`away_score` AS `away_score`,
                `raw_picks`.`home_score` AS `home_score`,
                `raw_picks`.`week` AS `week`,
                `raw_picks`.`changeable` AS `changeable`,
                `raw_picks`.`user` AS `user`,
                `raw_picks`.`away_team_name` AS `away_team_name`,
                `raw_picks`.`home_team_name` AS `home_team_name`,
                ABS((COALESCE(`raw_picks`.`home_pick`, 0) - COALESCE(`raw_picks`.`away_pick`, 0))) AS `user_margin`,
                (`raw_picks`.`home_pick` + `raw_picks`.`away_pick`) AS `user_total_score`,
                (CASE
                    WHEN (`raw_picks`.`home_pick` > `raw_picks`.`away_pick`) THEN `raw_picks`.`home_team_name`
                    WHEN (`raw_picks`.`away_pick` > `raw_picks`.`home_pick`) THEN `raw_picks`.`away_team_name`
                    ELSE 'TIE'
                END) AS `user_winner`,
                ABS((COALESCE(`raw_picks`.`home_score`, 0) - COALESCE(`raw_picks`.`away_score`, 0))) AS `actual_margin`,
                (`raw_picks`.`home_score` + `raw_picks`.`away_score`) AS `actual_total_score`,
                (CASE
                    WHEN
                        (ISNULL(`raw_picks`.`home_score`)
                            OR ISNULL(`raw_picks`.`away_score`))
                    THEN
                        'NULL'
                    WHEN (`raw_picks`.`home_score` > `raw_picks`.`away_score`) THEN `raw_picks`.`home_team_name`
                    WHEN (`raw_picks`.`away_score` > `raw_picks`.`home_score`) THEN `raw_picks`.`away_team_name`
                    ELSE 'TIE'
                END) AS `actual_winner`
        FROM
            (SELECT
            `p`.`id` AS `pick_id`,
                `f`.`ko_datetime` AS `ko_datetime`,
                (CASE
                    WHEN ISNULL(`p`.`home_pick`) THEN 30
                    ELSE `p`.`home_pick`
                END) AS `home_pick`,
                (CASE
                    WHEN ISNULL(`p`.`away_pick`) THEN 20
                    ELSE `p`.`away_pick`
                END) AS `away_pick`,
                `p`.`lock` AS `locked`,
                `f`.`away_score` AS `away_score`,
                `f`.`home_score` AS `home_score`,
                `f`.`week` AS `week`,
                `f`.`changeable` AS `changeable`,
                `u`.`id` AS `user`,
                `away`.`team_name` AS `away_team_name`,
                `home`.`team_name` AS `home_team_name`
        FROM
            ((((`nflpredictor$predictorDB`.`picks_pick` `p`
        LEFT JOIN `nflpredictor$predictorDB`.`fixtures_fixture` `f` ON ((`p`.`fixture_id` = `f`.`id`)))
        JOIN `nflpredictor$predictorDB`.`auth_user` `u` ON ((`u`.`id` = `p`.`user_id`)))
        LEFT JOIN `nflpredictor$predictorDB`.`fixtures_team` `away` ON ((`away`.`id` = `f`.`away_team_id`)))
        LEFT JOIN `nflpredictor$predictorDB`.`fixtures_team` `home` ON ((`home`.`id` = `f`.`home_team_id`)))) `raw_picks`) `predictions`) `points`)