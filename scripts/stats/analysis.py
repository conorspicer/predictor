#! /usr/bin/env python3
"""
Author: Conor Spicer
Date Created: 4th Jan 2018
"""
import nflgame
import numpy as np
import pandas as pd

data = pd.read_csv('2009_to_2017_data_complete.csv', index_col=0)
data
X = data[['team', 'week']]
