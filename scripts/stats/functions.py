"""
Author: Conor Spicer
Date Created: 4th Jan 2018
"""
fields = [
"game_id",
"team",
"home_away",
"pts_scored_last_5_games",
"pts_scored_season",
"pts_conceded_last_5_games",
"pts_conceded_season",
"totalyYds_gained_last_5",
"totalyYds_gained_season",
"passing_yds_gained_last_5",
"passing_yds_gained_season",
"rushing_yds_gained_last_5",
"rushing_yds_gained_season",
"totalyYds_allowed_last_5",
"totalyYds_allowed_season",
"passing_yds_allowed_last_5",
"passing_yds_allowed_season",
"rushing_yds_allowed_last_5",
"rushing_yds_allowed_season",
"penalty_yds_awarded_last_5",
"penalty_yds_awarded_season",
"penalty_yds_conceded_last_5",
"penalty_yds_conceded_season",
"first_downs_gained_last_5",
"first_downs_gained_season",
"first_downs_conceded_last_5",
"first_downs_conceded_season",
"turnovers_won_last_5",
"turnovers_won_season",
"turnovers_conceded_last_5",
"turnovers_conceded_season",
"opp_team",
"opp_pts_scored_last_5_games",
"opp_pts_scored_season",
"opp_pts_conceded_last_5_games",
"opp_pts_conceded_season",
"opp_totalyYds_gained_last_5",
"opp_totalyYds_gained_season",
"opp_passing_yds_gained_last_5",
"opp_passing_yds_gained_season",
"opp_rushing_yds_gained_last_5",
"opp_rushing_yds_gained_season",
"opp_totalyYds_allowed_last_5",
"opp_totalyYds_allowed_season",
"opp_passing_yds_allowed_last_5",
"opp_passing_yds_allowed_season",
"opp_rushing_yds_allowed_last_5",
"opp_rushing_yds_allowed_season",
"opp_penalty_yds_awarded_last_5",
"opp_penalty_yds_awarded_season",
"opp_penalty_yds_conceded_last_5",
"opp_penalty_yds_conceded_season",
"opp_first_downs_gained_last_5",
"opp_first_downs_gained_season",
"opp_first_downs_conceded_last_5",
"opp_first_downs_conceded_season",
"opp_turnovers_won_last_5",
"opp_turnovers_won_season",
"opp_turnovers_conceded_last_5",
"opp_turnovers_conceded_season",
]

independent_vars = ['home_away',
'pts_scored_last_5_games',
'pts_scored_season',
'pts_conceded_last_5_games',
'pts_conceded_season',
'totalyYds_gained_last_5',
'totalyYds_gained_season',
'passing_yds_gained_last_5',
'passing_yds_gained_season',
'rushing_yds_gained_last_5',
'rushing_yds_gained_season',
'totalyYds_allowed_last_5',
'totalyYds_allowed_season',
'passing_yds_allowed_last_5',
'passing_yds_allowed_season',
'rushing_yds_allowed_last_5',
'rushing_yds_allowed_season',
'penalty_yds_awarded_last_5',
'penalty_yds_awarded_season',
'penalty_yds_conceded_last_5',
'penalty_yds_conceded_season',
'first_downs_gained_last_5',
'first_downs_gained_season',
'first_downs_conceded_last_5',
'first_downs_conceded_season',
'turnovers_won_last_5',
'turnovers_won_season',
'turnovers_conceded_last_5',
'turnovers_conceded_season',
'opp_pts_scored_last_5_games',
'opp_pts_scored_season',
'opp_pts_conceded_last_5_games',
'opp_pts_conceded_season',
'opp_totalyYds_gained_last_5',
'opp_totalyYds_gained_season',
'opp_passing_yds_gained_last_5',
'opp_passing_yds_gained_season',
'opp_rushing_yds_gained_last_5',
'opp_rushing_yds_gained_season',
'opp_totalyYds_allowed_last_5',
'opp_totalyYds_allowed_season',
'opp_passing_yds_allowed_last_5',
'opp_passing_yds_allowed_season',
'opp_rushing_yds_allowed_last_5',
'opp_rushing_yds_allowed_season',
'opp_penalty_yds_awarded_last_5',
'opp_penalty_yds_awarded_season',
'opp_penalty_yds_conceded_last_5',
'opp_penalty_yds_conceded_season',
'opp_first_downs_gained_last_5',
'opp_first_downs_gained_season',
'opp_first_downs_conceded_last_5',
'opp_first_downs_conceded_season',
'opp_turnovers_won_last_5',
'opp_turnovers_won_season',
'opp_turnovers_conceded_last_5',
'opp_turnovers_conceded_season',
]

import nflgame
def last_5_weeks(week):
    if week > 4:
        weeks = list(range(week-5, week))
    else:
        weeks = list(range(1, week))
    return weeks

def weeks_so_far(week):
    return list(range(1, week))

def stats_avg(team, stat, year, week, timeframe='season'):
    if timeframe == 'last_5_weeks':
        weeks = last_5_weeks(week)
    else:
        weeks = weeks_so_far(week)
    try:
        home_games = nflgame.games(year=year, home=team, week=weeks, kind='REG')
    except:
        home_games = []
        # print("No home games in range")
    try:
        away_games = nflgame.games(year=year, away=team, week=weeks, kind='REG')
    except:
        away_games = []
        # print("No home games in range")
    value = 0
    if stat=='points_scored':
        for h in home_games:
            value += h.score_home
        for a in away_games:
            value += a.score_away
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='points_conceded':
        for h in home_games:
            value += h.score_away
        for a in away_games:
            value += a.score_home
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='total_yds_gained':
        for h in home_games:
            value += h.stats_home.total_yds
        for a in away_games:
            value += a.stats_away.total_yds
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='total_yds_allowed':
        for h in home_games:
            value += h.stats_away.total_yds
        for a in away_games:
            value += a.stats_home.total_yds
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='passing_yds_gained':
        for h in home_games:
            value += h.stats_home.passing_yds
        for a in away_games:
            value += a.stats_away.passing_yds
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='passing_yds_allowed':
        for h in home_games:
            value += h.stats_away.passing_yds
        for a in away_games:
            value += a.stats_home.passing_yds
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='rushing_yds_gained':
        for h in home_games:
            value += h.stats_home.rushing_yds
        for a in away_games:
            value += a.stats_away.rushing_yds
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='rushing_yds_allowed':
        for h in home_games:
            value += h.stats_away.rushing_yds
        for a in away_games:
            value += a.stats_home.rushing_yds
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='penalty_yds_awarded':
        for h in home_games:
            value += h.stats_home.penalty_yds
        for a in away_games:
            value += a.stats_away.penalty_yds
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='penalty_yds_conceded':
        for h in home_games:
            value += h.stats_away.penalty_yds
        for a in away_games:
            value += a.stats_home.penalty_yds
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='first_downs_gained':
        for h in home_games:
            value += h.stats_home.first_downs
        for a in away_games:
            value += a.stats_away.first_downs
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='first_downs_allowed':
        for h in home_games:
            value += h.stats_away.first_downs
        for a in away_games:
            value += a.stats_home.first_downs
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='turnovers_conceded':
        for h in home_games:
            value += h.stats_home.turnovers
        for a in away_games:
            value += a.stats_away.turnovers
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    if stat=='turnovers_won':
        for h in home_games:
            value += h.stats_away.turnovers
        for a in away_games:
            value += a.stats_home.turnovers
        if len(home_games + away_games)>0:
            value /= len(home_games + away_games)
        else:
            value = 0
    return value
