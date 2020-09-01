-- Make all fixtures no longer changable, so they do not appear in django views
UPDATE fixtures_fixture
SET changeable = 0
WHERE ko_datetime < current_date() AND id is not NULL;

-- Remove all playoff picks
UPDATE playoff_teams_playoffpick
SET
 afc_east_id=NULL,
 afc_north_id=NULL,
 afc_south_id=NULL,
 afc_west_id=NULL,
 afc_wild1_id=NULL,
 afc_wild2_id=NULL,
 nfc_east_id=NULL,
 nfc_north_id=NULL,
 nfc_south_id=NULL,
 nfc_west_id=NULL,
 nfc_wild1_id=NULL,
 nfc_wild2_id=NULL,
 sb_runner_up_id=NULL,
 sb_winner_id=NULL;