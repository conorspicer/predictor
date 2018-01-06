#! /usr/bin/env python3
"""
Author: Conor Spicer
Date Created: 4th Jan 2018

To refresh fixtures:
cd /Users/conorspicer/anaconda/envs/nflpenv/lib/python3.6/site-packages/nflgame
python update_sched.py --year 2017
"""
import nflgame
import numpy as np
import pandas as pd
import sys
sys.path.append('/Users/conorspicer/Documents/Udemy/Django/My_code/predictor/scripts/stats')
from functions import stats_avg
from functions import fields

games = nflgame.games(year = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017], kind='REG')
# games = nflgame.games(year = 2016, kind='REG')

# Create a pandas DataFrame in which to store our data:
data = pd.DataFrame(columns=fields)

for g in games:
    home_stats = {
    'game_id':g.gamekey,
    'team':g.home,
    'home_away':'home',
    'pts_scored_last_5_games':stats_avg(g.home,'points_scored',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'pts_scored_season':stats_avg(g.home,'points_scored',g.schedule['year'],g.schedule['week']),
    'pts_conceded_last_5_games':stats_avg(g.home,'points_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'pts_conceded_season':stats_avg(g.home,'points_conceded',g.schedule['year'],g.schedule['week']),
    'totalyYds_gained_last_5':stats_avg(g.home,'total_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'totalyYds_gained_season':stats_avg(g.home,'total_yds_gained',g.schedule['year'],g.schedule['week']),
    'passing_yds_gained_last_5':stats_avg(g.home,'passing_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'passing_yds_gained_season':stats_avg(g.home,'passing_yds_gained',g.schedule['year'],g.schedule['week']),
    'rushing_yds_gained_last_5':stats_avg(g.home,'rushing_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'rushing_yds_gained_season':stats_avg(g.home,'rushing_yds_gained',g.schedule['year'],g.schedule['week']),
    'totalyYds_allowed_last_5':stats_avg(g.home,'total_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'totalyYds_allowed_season':stats_avg(g.home,'total_yds_allowed',g.schedule['year'],g.schedule['week']),
    'passing_yds_allowed_last_5':stats_avg(g.home,'passing_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'passing_yds_allowed_season':stats_avg(g.home,'passing_yds_allowed',g.schedule['year'],g.schedule['week']),
    'rushing_yds_allowed_last_5':stats_avg(g.home,'rushing_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'rushing_yds_allowed_season':stats_avg(g.home,'rushing_yds_allowed',g.schedule['year'],g.schedule['week']),
    'penalty_yds_awarded_last_5':stats_avg(g.home,'penalty_yds_awarded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'penalty_yds_awarded_season':stats_avg(g.home,'penalty_yds_awarded',g.schedule['year'],g.schedule['week']),
    'penalty_yds_conceded_last_5':stats_avg(g.home,'penalty_yds_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'penalty_yds_conceded_season':stats_avg(g.home,'penalty_yds_conceded',g.schedule['year'],g.schedule['week']),
    'first_downs_gained_last_5':stats_avg(g.home,'first_downs_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'first_downs_gained_season':stats_avg(g.home,'first_downs_gained',g.schedule['year'],g.schedule['week']),
    'first_downs_conceded_last_5':stats_avg(g.home,'first_downs_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'first_downs_conceded_season':stats_avg(g.home,'first_downs_allowed',g.schedule['year'],g.schedule['week']),
    'turnovers_won_last_5':stats_avg(g.home,'turnovers_won',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'turnovers_won_season':stats_avg(g.home,'turnovers_won',g.schedule['year'],g.schedule['week']),
    'turnovers_conceded_last_5':stats_avg(g.home,'turnovers_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'turnovers_conceded_season':stats_avg(g.home,'turnovers_conceded',g.schedule['year'],g.schedule['week']),
    'opp_team':g.away,
    'opp_pts_scored_last_5_games':stats_avg(g.away,'points_scored',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_pts_scored_season':stats_avg(g.away,'points_scored',g.schedule['year'],g.schedule['week']),
    'opp_pts_conceded_last_5_games':stats_avg(g.away,'points_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_pts_conceded_season':stats_avg(g.away,'points_conceded',g.schedule['year'],g.schedule['week']),
    'opp_totalyYds_gained_last_5':stats_avg(g.away,'total_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_totalyYds_gained_season':stats_avg(g.away,'total_yds_gained',g.schedule['year'],g.schedule['week']),
    'opp_passing_yds_gained_last_5':stats_avg(g.away,'passing_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_passing_yds_gained_season':stats_avg(g.away,'passing_yds_gained',g.schedule['year'],g.schedule['week']),
    'opp_rushing_yds_gained_last_5':stats_avg(g.away,'rushing_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_rushing_yds_gained_season':stats_avg(g.away,'rushing_yds_gained',g.schedule['year'],g.schedule['week']),
    'opp_totalyYds_allowed_last_5':stats_avg(g.away,'total_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_totalyYds_allowed_season':stats_avg(g.away,'total_yds_allowed',g.schedule['year'],g.schedule['week']),
    'opp_passing_yds_allowed_last_5':stats_avg(g.away,'passing_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_passing_yds_allowed_season':stats_avg(g.away,'passing_yds_allowed',g.schedule['year'],g.schedule['week']),
    'opp_rushing_yds_allowed_last_5':stats_avg(g.away,'rushing_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_rushing_yds_allowed_season':stats_avg(g.away,'rushing_yds_allowed',g.schedule['year'],g.schedule['week']),
    'opp_penalty_yds_awarded_last_5':stats_avg(g.away,'penalty_yds_awarded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_penalty_yds_awarded_season':stats_avg(g.away,'penalty_yds_awarded',g.schedule['year'],g.schedule['week']),
    'opp_penalty_yds_conceded_last_5':stats_avg(g.away,'penalty_yds_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_penalty_yds_conceded_season':stats_avg(g.away,'penalty_yds_conceded',g.schedule['year'],g.schedule['week']),
    'opp_first_downs_gained_last_5':stats_avg(g.away,'first_downs_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_first_downs_gained_season':stats_avg(g.away,'first_downs_gained',g.schedule['year'],g.schedule['week']),
    'opp_first_downs_conceded_last_5':stats_avg(g.away,'first_downs_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_first_downs_conceded_season':stats_avg(g.away,'first_downs_allowed',g.schedule['year'],g.schedule['week']),
    'opp_turnovers_won_last_5':stats_avg(g.away,'turnovers_won',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_turnovers_won_season':stats_avg(g.away,'turnovers_won',g.schedule['year'],g.schedule['week']),
    'opp_turnovers_conceded_last_5':stats_avg(g.away,'turnovers_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_turnovers_conceded_season':stats_avg(g.away,'turnovers_conceded',g.schedule['year'],g.schedule['week'])
    }
    data = data.append(home_stats, ignore_index=True)

for g in games:
    away_stats = {
    'game_id':g.gamekey,
    'team':g.away,
    'home_away':'home',
    'pts_scored_last_5_games':stats_avg(g.away,'points_scored',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'pts_scored_season':stats_avg(g.away,'points_scored',g.schedule['year'],g.schedule['week']),
    'pts_conceded_last_5_games':stats_avg(g.away,'points_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'pts_conceded_season':stats_avg(g.away,'points_conceded',g.schedule['year'],g.schedule['week']),
    'totalyYds_gained_last_5':stats_avg(g.away,'total_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'totalyYds_gained_season':stats_avg(g.away,'total_yds_gained',g.schedule['year'],g.schedule['week']),
    'passing_yds_gained_last_5':stats_avg(g.away,'passing_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'passing_yds_gained_season':stats_avg(g.away,'passing_yds_gained',g.schedule['year'],g.schedule['week']),
    'rushing_yds_gained_last_5':stats_avg(g.away,'rushing_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'rushing_yds_gained_season':stats_avg(g.away,'rushing_yds_gained',g.schedule['year'],g.schedule['week']),
    'totalyYds_allowed_last_5':stats_avg(g.away,'total_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'totalyYds_allowed_season':stats_avg(g.away,'total_yds_allowed',g.schedule['year'],g.schedule['week']),
    'passing_yds_allowed_last_5':stats_avg(g.away,'passing_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'passing_yds_allowed_season':stats_avg(g.away,'passing_yds_allowed',g.schedule['year'],g.schedule['week']),
    'rushing_yds_allowed_last_5':stats_avg(g.away,'rushing_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'rushing_yds_allowed_season':stats_avg(g.away,'rushing_yds_allowed',g.schedule['year'],g.schedule['week']),
    'penalty_yds_awarded_last_5':stats_avg(g.away,'penalty_yds_awarded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'penalty_yds_awarded_season':stats_avg(g.away,'penalty_yds_awarded',g.schedule['year'],g.schedule['week']),
    'penalty_yds_conceded_last_5':stats_avg(g.away,'penalty_yds_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'penalty_yds_conceded_season':stats_avg(g.away,'penalty_yds_conceded',g.schedule['year'],g.schedule['week']),
    'first_downs_gained_last_5':stats_avg(g.away,'first_downs_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'first_downs_gained_season':stats_avg(g.away,'first_downs_gained',g.schedule['year'],g.schedule['week']),
    'first_downs_conceded_last_5':stats_avg(g.away,'first_downs_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'first_downs_conceded_season':stats_avg(g.away,'first_downs_allowed',g.schedule['year'],g.schedule['week']),
    'turnovers_won_last_5':stats_avg(g.away,'turnovers_won',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'turnovers_won_season':stats_avg(g.away,'turnovers_won',g.schedule['year'],g.schedule['week']),
    'turnovers_conceded_last_5':stats_avg(g.away,'turnovers_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'turnovers_conceded_season':stats_avg(g.away,'turnovers_conceded',g.schedule['year'],g.schedule['week']),
    'opp_team':g.home,
    'opp_pts_scored_last_5_games':stats_avg(g.home,'points_scored',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_pts_scored_season':stats_avg(g.home,'points_scored',g.schedule['year'],g.schedule['week']),
    'opp_pts_conceded_last_5_games':stats_avg(g.home,'points_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_pts_conceded_season':stats_avg(g.home,'points_conceded',g.schedule['year'],g.schedule['week']),
    'opp_totalyYds_gained_last_5':stats_avg(g.home,'total_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_totalyYds_gained_season':stats_avg(g.home,'total_yds_gained',g.schedule['year'],g.schedule['week']),
    'opp_passing_yds_gained_last_5':stats_avg(g.home,'passing_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_passing_yds_gained_season':stats_avg(g.home,'passing_yds_gained',g.schedule['year'],g.schedule['week']),
    'opp_rushing_yds_gained_last_5':stats_avg(g.home,'rushing_yds_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_rushing_yds_gained_season':stats_avg(g.home,'rushing_yds_gained',g.schedule['year'],g.schedule['week']),
    'opp_totalyYds_allowed_last_5':stats_avg(g.home,'total_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_totalyYds_allowed_season':stats_avg(g.home,'total_yds_allowed',g.schedule['year'],g.schedule['week']),
    'opp_passing_yds_allowed_last_5':stats_avg(g.home,'passing_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_passing_yds_allowed_season':stats_avg(g.home,'passing_yds_allowed',g.schedule['year'],g.schedule['week']),
    'opp_rushing_yds_allowed_last_5':stats_avg(g.home,'rushing_yds_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_rushing_yds_allowed_season':stats_avg(g.home,'rushing_yds_allowed',g.schedule['year'],g.schedule['week']),
    'opp_penalty_yds_awarded_last_5':stats_avg(g.home,'penalty_yds_awarded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_penalty_yds_awarded_season':stats_avg(g.home,'penalty_yds_awarded',g.schedule['year'],g.schedule['week']),
    'opp_penalty_yds_conceded_last_5':stats_avg(g.home,'penalty_yds_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_penalty_yds_conceded_season':stats_avg(g.home,'penalty_yds_conceded',g.schedule['year'],g.schedule['week']),
    'opp_first_downs_gained_last_5':stats_avg(g.home,'first_downs_gained',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_first_downs_gained_season':stats_avg(g.home,'first_downs_gained',g.schedule['year'],g.schedule['week']),
    'opp_first_downs_conceded_last_5':stats_avg(g.home,'first_downs_allowed',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_first_downs_conceded_season':stats_avg(g.home,'first_downs_allowed',g.schedule['year'],g.schedule['week']),
    'opp_turnovers_won_last_5':stats_avg(g.home,'turnovers_won',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_turnovers_won_season':stats_avg(g.home,'turnovers_won',g.schedule['year'],g.schedule['week']),
    'opp_turnovers_conceded_last_5':stats_avg(g.home,'turnovers_conceded',g.schedule['year'],g.schedule['week'],'last_5_weeks'),
    'opp_turnovers_conceded_season':stats_avg(g.home,'turnovers_conceded',g.schedule['year'],g.schedule['week'])
    }
    data = data.append(away_stats, ignore_index=True)
    print(g.schedule['year'])

data.to_csv('2009_to_2017_data.csv')
