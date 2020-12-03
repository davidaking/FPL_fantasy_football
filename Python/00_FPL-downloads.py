# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 19:01:37 2020

Script to access FPL information

Reference:
https://towardsdatascience.com/fantasy-premier-league-value-analysis-python-tutorial-using-the-fpl-api-8031edfe9910


@author: david
"""

import requests
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

json_data = requests.get(url).json()


df_elem = pd.DataFrame(json_data['elements'])
df_elem_type = pd.DataFrame(json_data['element_types'])
df_teams = pd.DataFrame(json_data['teams'])


filter_cols = ['id','second_name','team','element_type','selected_by_percent','now_cost','minutes','transfers_in','value_season','total_points']

df_elem_filter = df_elem[filter_cols]

# sort by points
df_sort = df_elem_filter.sort_values('total_points',ascending = False)

df_sort['now_cost'] = df_sort['now_cost'] / 10



df_teams_id = df_teams.loc[:,['id','short_name']]

ind_pos = list(df_elem_type.columns).index('plural_name')

# Position list
pos_list = [df_elem_type.iloc[i,ind_pos] for i in df_elem_type.index]

# Element type for all players
elem_list = [df_sort.loc[i,'element_type'] for i in df_sort.index]

# Map element type to position and add as column to df_sort
df_sort['position'] = [pos_list[i-1] for i in elem_list]


ind_pos = list(df_teams_id.columns).index('short_name')
# Team list
team_list = [df_teams_id.iloc[i,ind_pos] for i in df_teams_id.index]

# Team for all players
elem_list = [df_sort.loc[i,'team'] for i in df_sort.index]


# Map element type to position and add as column to df_sort
df_sort['team_name'] = [team_list[i-1] for i in elem_list]

# Create points / cost (same as value_season but numeric)
df_sort['points_to_cost'] = df_sort['total_points'] / df_sort['now_cost']



# Add fixture difficulty for next fixture_lookahead games
fixture_lookahead = 5

difficulty_list = []
id_list = df_sort['id'].tolist()

for player_id in id_list:

#url = 'https://fantasy.premierleague.com/api/element-summary/110/'
    url = f'https://fantasy.premierleague.com/api/element-summary/{player_id}/'
    json_data = requests.get(url).json()
    df_1 = pd.DataFrame(json_data['fixtures'])
    difficulty_list.append(sum(df_1.head(fixture_lookahead)['difficulty']))

df_sort['difficulty'] = difficulty_list


# Export data to SQLite
export_file = f'sqlite:///{data_dir}FPL-player-stats.db'
engine = create_engine(export_file, echo=False)

conn =  engine.connect()
df_sort.to_sql('player_stats', conn,if_exists='replace')

# Close connection
conn.close()









