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


-- Write new fixtures to DB
INSERT INTO fixtures_fixture(name,week,ko_datetime,changeable,away_team_id,home_team_id,away_score,home_score)
VALUES
(2020002,1,"2020/09/13 17:00",1,50,51,0,0),
(2020003,1,"2020/09/13 17:00",1,64,38,0,0),
(2020004,1,"2020/09/13 17:00",1,60,41,0,0),
(2020005,1,"2020/09/13 17:00",1,61,68,0,0),
(2020006,1,"2020/09/13 17:00",1,44,39,0,0),
(2020007,1,"2020/09/13 17:00",1,48,55,0,0),
(2020008,1,"2020/09/13 17:00",1,42,47,0,0),
(2020009,1,"2020/09/13 17:00",1,54,56,0,0),
(2020010,1,"2020/09/13 17:00",1,59,40,0,0),
(2020011,1,"2020/09/13 20:05",1,63,43,0,0),
(2020012,1,"2020/09/13 20:25",1,37,65,0,0),
(2020013,1,"2020/09/13 20:25",1,66,57,0,0),
(2020014,1,"2020/09/14 00:20",1,45,53,0,0),
(2020015,1,"2020/09/14 23:15",1,62,58,0,0),
(2020016,1,"2020/09/15 02:10",1,67,46,0,0),
(2020017,2,"2020/09/18 00:20",1,43,44,0,0),
(2020018,2,"2020/09/20 17:00",1,53,61,0,0),
(2020019,2,"2020/09/20 17:00",1,38,45,0,0),
(2020020,2,"2020/09/20 17:00",1,51,67,0,0),
(2020021,2,"2020/09/20 17:00",1,65,59,0,0),
(2020022,2,"2020/09/20 17:00",1,40,54,0,0),
(2020023,2,"2020/09/20 17:00",1,55,50,0,0),
(2020024,2,"2020/09/20 17:00",1,58,42,0,0),
(2020025,2,"2020/09/20 17:00",1,41,66,0,0),
(2020026,2,"2020/09/20 17:00",1,46,62,0,0),
(2020027,2,"2020/09/20 17:00",1,47,48,0,0),
(2020028,2,"2020/09/20 20:05",1,68,37,0,0),
(2020029,2,"2020/09/20 20:25",1,52,63,0,0),
(2020030,2,"2020/09/20 20:25",1,39,49,0,0),
(2020031,2,"2020/09/21 00:20",1,56,64,0,0),
(2020032,2,"2020/09/22 00:15",1,57,60,0,0),
(2020033,3,"2020/09/25 00:20",1,54,51,0,0),
(2020034,3,"2020/09/27 17:00",1,43,61,0,0),
(2020035,3,"2020/09/27 17:00",1,65,58,0,0),
(2020036,3,"2020/09/27 17:00",1,68,44,0,0),
(2020037,3,"2020/09/27 17:00",1,60,56,0,0),
(2020038,3,"2020/09/27 17:00",1,42,38,0,0),
(2020039,3,"2020/09/27 17:00",1,49,62,0,0),
(2020040,3,"2020/09/27 17:00",1,67,55,0,0),
(2020041,3,"2020/09/27 17:00",1,53,40,0,0),
(2020042,3,"2020/09/27 20:05",1,59,50,0,0),
(2020043,3,"2020/09/27 20:05",1,41,63,0,0),
(2020044,3,"2020/09/27 20:25",1,45,64,0,0),
(2020045,3,"2020/09/27 20:25",1,66,46,0,0),
(2020046,3,"2020/09/27 20:25",1,47,37,0,0),
(2020047,3,"2020/09/28 00:20",1,48,57,0,0),
(2020048,3,"2020/09/29 00:15",1,52,39,0,0),
(2020049,4,"2020/10/02 00:20",1,46,59,0,0),
(2020050,4,"2020/10/04 17:00",1,63,66,0,0),
(2020051,4,"2020/10/04 17:00",1,64,54,0,0),
(2020052,4,"2020/10/04 17:00",1,50,42,0,0),
(2020053,4,"2020/10/04 17:00",1,62,67,0,0),
(2020054,4,"2020/10/04 17:00",1,55,49,0,0),
(2020055,4,"2020/10/04 17:00",1,57,47,0,0),
(2020056,4,"2020/10/04 17:00",1,39,68,0,0),
(2020057,4,"2020/10/04 17:00",1,44,45,0,0),
(2020058,4,"2020/10/04 17:00",1,37,41,0,0),
(2020059,4,"2020/10/04 17:00",1,51,43,0,0),
(2020060,4,"2020/10/04 20:05",1,58,53,0,0),
(2020061,4,"2020/10/04 20:25",1,56,52,0,0),
(2020062,4,"2020/10/04 20:25",1,40,60,0,0),
(2020063,4,"2020/10/05 00:20",1,61,65,0,0),
(2020064,4,"2020/10/06 00:15",1,38,48,0,0),
(2020065,5,"2020/10/09 00:20",1,66,42,0,0),
(2020066,5,"2020/10/11 17:00",1,53,68,0,0),
(2020067,5,"2020/10/11 17:00",1,40,67,0,0),
(2020068,5,"2020/10/11 17:00",1,61,62,0,0),
(2020069,5,"2020/10/11 17:00",1,51,49,0,0),
(2020070,5,"2020/10/11 17:00",1,46,56,0,0),
(2020071,5,"2020/10/11 17:00",1,37,59,0,0),
(2020072,5,"2020/10/11 17:00",1,43,39,0,0),
(2020073,5,"2020/10/11 17:00",1,60,52,0,0),
(2020074,5,"2020/10/11 17:00",1,41,38,0,0),
(2020075,5,"2020/10/11 20:05",1,54,65,0,0),
(2020076,5,"2020/10/11 20:25",1,58,45,0,0),
(2020077,5,"2020/10/11 20:25",1,50,44,0,0),
(2020078,5,"2020/10/12 00:20",1,55,64,0,0),
(2020079,5,"2020/10/13 00:15",1,63,57,0,0),
(2020080,6,"2020/10/16 00:20",1,52,40,0,0),
(2020081,6,"2020/10/18 17:00",1,43,50,0,0),
(2020082,6,"2020/10/18 17:00",1,47,51,0,0),
(2020083,6,"2020/10/18 17:00",1,38,55,0,0),
(2020084,6,"2020/10/18 17:00",1,42,41,0,0),
(2020085,6,"2020/10/18 17:00",1,68,58,0,0),
(2020086,6,"2020/10/18 17:00",1,49,67,0,0),
(2020087,6,"2020/10/18 17:00",1,39,61,0,0),
(2020088,6,"2020/10/18 17:00",1,44,62,0,0),
(2020089,6,"2020/10/18 20:05",1,59,63,0,0),
(2020090,6,"2020/10/18 20:05",1,54,46,0,0),
(2020091,6,"2020/10/18 20:25",1,48,66,0,0),
(2020092,6,"2020/10/19 00:20",1,53,65,0,0),
(2020093,6,"2020/10/20 00:15",1,37,45,0,0),
(2020094,7,"2020/10/23 00:20",1,58,61,0,0),
(2020095,7,"2020/10/25 17:00",1,45,68,0,0),
(2020096,7,"2020/10/25 17:00",1,63,54,0,0),
(2020097,7,"2020/10/25 17:00",1,48,49,0,0),
(2020098,7,"2020/10/25 17:00",1,41,57,0,0),
(2020099,7,"2020/10/25 17:00",1,47,38,0,0),
(2020100,7,"2020/10/25 17:00",1,62,39,0,0),
(2020101,7,"2020/10/25 17:00",1,40,59,0,0),
(2020102,7,"2020/10/25 17:00",1,44,43,0,0),
(2020103,7,"2020/10/25 20:05",1,64,37,0,0),
(2020104,7,"2020/10/25 20:25",1,65,56,0,0),
(2020105,7,"2020/10/25 20:25",1,52,46,0,0),
(2020106,7,"2020/10/26 00:20",1,66,60,0,0),
(2020107,7,"2020/10/27 00:15",1,42,53,0,0),
(2020108,8,"2020/10/30 00:20",1,38,41,0,0),
(2020109,8,"2020/11/01 18:00",1,55,48,0,0),
(2020110,8,"2020/11/01 18:00",1,50,47,0,0),
(2020111,8,"2020/11/01 18:00",1,59,52,0,0),
(2020112,8,"2020/11/01 18:00",1,67,43,0,0),
(2020113,8,"2020/11/01 18:00",1,56,40,0,0),
(2020114,8,"2020/11/01 18:00",1,60,44,0,0),
(2020115,8,"2020/11/01 18:00",1,53,54,0,0),
(2020116,8,"2020/11/01 21:05",1,51,63,0,0),
(2020117,8,"2020/11/01 21:25",1,57,42,0,0),
(2020118,8,"2020/11/01 21:25",1,65,64,0,0),
(2020119,8,"2020/11/02 01:20",1,45,61,0,0),
(2020120,8,"2020/11/03 01:15",1,66,58,0,0),
(2020121,9,"2020/11/06 01:20",1,48,65,0,0),
(2020122,9,"2020/11/08 18:00",1,58,68,0,0),
(2020123,9,"2020/11/08 18:00",1,49,51,0,0),
(2020124,9,"2020/11/08 18:00",1,46,38,0,0),
(2020125,9,"2020/11/08 18:00",1,42,67,0,0),
(2020126,9,"2020/11/08 18:00",1,47,55,0,0),
(2020127,9,"2020/11/08 18:00",1,41,52,0,0),
(2020128,9,"2020/11/08 18:00",1,39,50,0,0),
(2020129,9,"2020/11/08 18:00",1,64,40,0,0),
(2020130,9,"2020/11/08 21:05",1,60,63,0,0),
(2020131,9,"2020/11/08 21:25",1,54,37,0,0),
(2020132,9,"2020/11/08 21:25",1,62,45,0,0),
(2020133,9,"2020/11/09 01:20",1,57,66,0,0),
(2020134,9,"2020/11/10 01:15",1,56,59,0,0),
(2020135,10,"2020/11/13 01:20",1,50,67,0,0),
(2020136,10,"2020/11/15 18:00",1,43,62,0,0),
(2020137,10,"2020/11/15 18:00",1,68,47,0,0),
(2020138,10,"2020/11/15 18:00",1,49,44,0,0),
(2020139,10,"2020/11/15 18:00",1,61,58,0,0),
(2020140,10,"2020/11/15 18:00",1,51,48,0,0),
(2020141,10,"2020/11/15 18:00",1,66,41,0,0),
(2020142,10,"2020/11/15 21:05",1,46,60,0,0),
(2020143,10,"2020/11/15 21:05",1,40,37,0,0),
(2020144,10,"2020/11/15 21:05",1,59,54,0,0),
(2020145,10,"2020/11/15 21:25",1,65,57,0,0),
(2020146,10,"2020/11/15 21:25",1,64,53,0,0),
(2020147,10,"2020/11/16 01:20",1,39,56,0,0),
(2020148,10,"2020/11/17 01:15",1,55,42,0,0),
(2020149,11,"2020/11/20 01:20",1,37,64,0,0),
(2020150,11,"2020/11/22 18:00",1,43,68,0,0),
(2020151,11,"2020/11/22 18:00",1,38,57,0,0),
(2020152,11,"2020/11/22 18:00",1,56,49,0,0),
(2020153,11,"2020/11/22 18:00",1,67,39,0,0),
(2020154,11,"2020/11/22 18:00",1,62,51,0,0),
(2020155,11,"2020/11/22 18:00",1,47,41,0,0),
(2020156,11,"2020/11/22 18:00",1,61,44,0,0),
(2020157,11,"2020/11/22 18:00",1,48,50,0,0),
(2020158,11,"2020/11/22 21:05",1,63,46,0,0),
(2020159,11,"2020/11/22 21:25",1,45,55,0,0),
(2020160,11,"2020/11/23 01:20",1,52,60,0,0),
(2020161,11,"2020/11/24 01:15",1,53,66,0,0),
(2020162,12,"2020/11/26 17:30",1,49,47,0,0),
(2020163,12,"2020/11/26 21:30",1,68,45,0,0),
(2020164,12,"2020/11/27 01:20",1,39,62,0,0),
(2020165,12,"2020/11/29 18:00",1,58,43,0,0),
(2020166,12,"2020/11/29 18:00",1,63,40,0,0),
(2020167,12,"2020/11/29 18:00",1,44,51,0,0),
(2020168,12,"2020/11/29 18:00",1,37,56,0,0),
(2020169,12,"2020/11/29 18:00",1,67,50,0,0),
(2020170,12,"2020/11/29 18:00",1,41,55,0,0),
(2020171,12,"2020/11/29 18:00",1,54,59,0,0),
(2020172,12,"2020/11/29 18:00",1,60,38,0,0),
(2020173,12,"2020/11/29 21:05",1,65,53,0,0),
(2020174,12,"2020/11/29 21:05",1,57,46,0,0),
(2020175,12,"2020/11/29 21:25",1,52,66,0,0),
(2020176,12,"2020/11/30 01:20",1,42,48,0,0),
(2020177,12,"2020/12/01 01:15",1,64,61,0,0),
(2020178,13,"2020/12/04 01:20",1,45,39,0,0),
(2020179,13,"2020/12/06 18:00",1,50,49,0,0),
(2020180,13,"2020/12/06 18:00",1,68,62,0,0),
(2020181,13,"2020/12/06 18:00",1,60,59,0,0),
(2020182,13,"2020/12/06 18:00",1,51,55,0,0),
(2020183,13,"2020/12/06 18:00",1,57,38,0,0),
(2020184,13,"2020/12/06 18:00",1,44,67,0,0),
(2020185,13,"2020/12/06 18:00",1,43,54,0,0),
(2020186,13,"2020/12/06 18:00",1,47,42,0,0),
(2020187,13,"2020/12/06 21:05",1,58,64,0,0),
(2020188,13,"2020/12/06 21:05",1,53,37,0,0),
(2020189,13,"2020/12/06 21:25",1,56,63,0,0),
(2020190,13,"2020/12/06 21:25",1,61,48,0,0),
(2020191,13,"2020/12/07 01:20",1,46,52,0,0),
(2020192,13,"2020/12/08 01:15",1,40,65,0,0),
(2020193,14,"2020/12/11 01:20",1,56,53,0,0),
(2020194,14,"2020/12/13 18:00",1,49,42,0,0),
(2020195,14,"2020/12/13 18:00",1,67,51,0,0),
(2020196,14,"2020/12/13 18:00",1,55,66,0,0),
(2020197,14,"2020/12/13 18:00",1,37,58,0,0),
(2020198,14,"2020/12/13 18:00",1,52,54,0,0),
(2020199,14,"2020/12/13 18:00",1,45,43,0,0),
(2020200,14,"2020/12/13 18:00",1,48,47,0,0),
(2020201,14,"2020/12/13 18:00",1,46,41,0,0),
(2020202,14,"2020/12/13 21:05",1,59,64,0,0),
(2020203,14,"2020/12/13 21:05",1,50,60,0,0),
(2020204,14,"2020/12/13 21:25",1,68,65,0,0),
(2020205,14,"2020/12/13 21:25",1,57,61,0,0),
(2020206,14,"2020/12/13 21:25",1,38,63,0,0),
(2020207,14,"2020/12/14 01:20",1,62,40,0,0),
(2020208,14,"2020/12/15 01:15",1,39,44,0,0),
(2020209,15,"2020/12/18 01:20",1,63,60,0,0),
(2020210,15,"2020/12/19 18:00",1,47,67,0,0),
(2020211,15,"2020/12/19 18:00",1,59,53,0,0),
(2020212,15,"2020/12/19 18:00",1,41,48,0,0),
(2020213,15,"2020/12/19 18:00",1,49,50,0,0),
(2020214,15,"2020/12/19 18:00",1,40,46,0,0),
(2020215,15,"2020/12/20 18:00",1,51,39,0,0),
(2020216,15,"2020/12/20 18:00",1,66,38,0,0),
(2020217,15,"2020/12/20 18:00",1,64,68,0,0),
(2020218,15,"2020/12/20 18:00",1,44,58,0,0),
(2020219,15,"2020/12/20 18:00",1,42,55,0,0),
(2020220,15,"2020/12/20 18:00",1,56,54,0,0),
(2020221,15,"2020/12/20 21:05",1,61,37,0,0),
(2020222,15,"2020/12/20 21:25",1,52,57,0,0),
(2020223,15,"2020/12/21 01:20",1,65,45,0,0),
(2020224,15,"2020/12/22 01:15",1,62,43,0,0),
(2020225,16,"2020/12/25 21:30",1,55,57,0,0),
(2020226,16,"2020/12/26 18:00",1,46,63,0,0),
(2020227,16,"2020/12/26 18:00",1,54,60,0,0),
(2020228,16,"2020/12/26 18:00",1,44,59,0,0),
(2020229,16,"2020/12/26 18:00",1,65,37,0,0),
(2020230,16,"2020/12/26 18:00",1,66,47,0,0),
(2020231,16,"2020/12/27 18:00",1,42,51,0,0),
(2020232,16,"2020/12/27 18:00",1,41,68,0,0),
(2020233,16,"2020/12/27 18:00",1,50,62,0,0),
(2020234,16,"2020/12/27 18:00",1,43,49,0,0),
(2020235,16,"2020/12/27 18:00",1,58,39,0,0),
(2020236,16,"2020/12/27 18:00",1,38,52,0,0),
(2020237,16,"2020/12/27 21:05",1,53,64,0,0),
(2020238,16,"2020/12/27 21:25",1,61,45,0,0),
(2020239,16,"2020/12/28 01:20",1,67,48,0,0),
(2020240,16,"2020/12/29 01:15",1,40,56,0,0),
(2020241,17,"2021/01/03 18:00",1,55,47,0,0),
(2020242,17,"2021/01/03 18:00",1,38,66,0,0),
(2020243,17,"2021/01/03 18:00",1,67,49,0,0),
(2020244,17,"2021/01/03 18:00",1,59,56,0,0),
(2020245,17,"2021/01/03 18:00",1,62,44,0,0),
(2020246,17,"2021/01/03 18:00",1,45,58,0,0),
(2020247,17,"2021/01/03 18:00",1,63,52,0,0),
(2020248,17,"2021/01/03 18:00",1,68,61,0,0),
(2020249,17,"2021/01/03 18:00",1,51,50,0,0),
(2020250,17,"2021/01/03 18:00",1,39,43,0,0),
(2020251,17,"2021/01/03 18:00",1,54,40,0,0),
(2020252,17,"2021/01/03 18:00",1,57,41,0,0),
(2020253,17,"2021/01/03 18:00",1,48,42,0,0),
(2020254,17,"2021/01/03 21:25",1,37,53,0,0),
(2020255,17,"2021/01/03 21:25",1,64,65,0,0),
(2020256,17,"2021/01/03 21:25",1,60,46,0,0)