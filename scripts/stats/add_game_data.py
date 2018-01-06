#! /usr/bin/env python3
"""
Author: Conor Spicer
Date Created: 4th Jan 2018
"""
import nflgame
import numpy as np
import pandas as pd

data = pd.read_csv('2009_to_2017_data.csv', index_col=0)

games = nflgame.games(year = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017], kind='REG')
new_fields = ['game_id', 'team','home_score', 'away_score', 'win', 'margin', 'total_pts', 'year', 'week']
extra_data = pd.DataFrame(columns=new_fields)

for g in games:
    if g.score_home>g.score_away:
        winner = g.home
    elif g.score_away>g.score_home:
        winner = g.away
    else:
        winner = 'TIE'
    home_stats = {
    'game_id':g.gamekey,
    'team':g.home,
    'home_score':g.score_home,
    'away_score':g.score_away,
    'win':winner==g.home,
    'margin':abs(g.score_home-g.score_away),
    'total_pts':abs(g.score_home+g.score_away),
    'year':g.schedule['year'],
    'week':g.schedule['week'],
    }
    extra_data = extra_data.append(home_stats, ignore_index=True)

extra_data
for g in games:
    if g.score_home>g.score_away:
        winner = g.home
    elif g.score_away>g.score_home:
        winner = g.away
    else:
        winner = 'TIE'
    away_stats = {
    'game_id':g.gamekey,
    'team':g.away,
    'home_score':g.score_home,
    'away_score':g.score_away,
    'win':winner==g.away,
    'margin':abs(g.score_home-g.score_away),
    'total_pts':abs(g.score_home+g.score_away),
    'year':g.schedule['year'],
    'week':g.schedule['week'],
    }
    extra_data = extra_data.append(away_stats, ignore_index=True)

    print(g.schedule['year'])

extra_data.to_csv('extra_data.csv')
