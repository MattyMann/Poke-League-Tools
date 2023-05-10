import math
from itertools import combinations
from random import shuffle
import pandas as pd
import numpy as np
import argparse
import os

season_num = 1

def create_conventions( rankings ) -> dict:

    # Read in the ratings for elo calc
    ratings = pd.read_parquet(rankings)
    
    ratings = ratings.sort_values('elo',ascending=False)
    
    # Create a new DF with just the active players
    active_players = ratings[ratings['active'] == True].drop(columns=['elo','active'])

    # Number of active players
    num_active_players = len(active_players)

    # Convention names, based on Pokeball names
    convnames = ['Master','Ultra','Great']
    
    # How many conventions should be made? By default we say there should be eight per convention
    num_of_conventions = min(math.ceil(num_active_players / 8),len(convnames))

    # How many players are 'active', i.e., will be playing this season
    active_players = active_players.to_numpy()
    
    # Create a list of conventions based on elo
    conventions = dict(zip(convnames,map(lambda conv: conv.tolist(),np.split(active_players,num_of_conventions))))

    # Make into lists
    for (name,convention) in conventions.items():
        
        conventions[name] = list(map(lambda player: player[0],convention))
        
    return conventions

def create_league_tables( conventions: dict):

    for (name,convention) in conventions.items():

        table = pd.DataFrame({'username': convention})

        table['wins'],table['losses'],table['draws'],table['points'],table['kills'],table['faints'],table['k/d'] = 0,0,0,0,0,0,0
        # This should work but is causing issues. It might be more efficient if we can get it to work.
        # table = table.reindex(columns=['wins','losses','draws','points','kills','faints','k/d'], fill_value=0)

        table = table.astype({'username': 'string', 'wins': 'int8', 'losses': 'int8', 'draws': 'int8','points':'int8','kills': 'int8', 'faints':'int8', 'k/d': 'int8'})

        table = table.sort_values(['points','k/d','wins'])
        
        os.makedir("seasons/season_"+str(season_num)+"/conference_" + name)

        table.to_parquet("seasons/season_"+str(season_num)+"/conference_" + name + "/table")

    with open("seasons/season_"+str(season_num)+"/index","a") as f:
        f.write(str(conventions))

def create_matches( convention: list ) -> list:

    # Get the number of players in the convention. If odd, add a 'Day Off' player and make even
    num_players = len(convention)

    if num_players % 2:
        convention.append('Day Off')
        num_players += 1

    # Number of days the tournament must last
    num_days = num_players - 1

    # Number of games per day
    games_per_day = num_players // 2

    # Create all matches
    match_list = list(combinations(convention,2))

    # Shuffle the matches
    shuffle(match_list)

    # This logic makes me want to die. It makes sure players only appear once each day, and all matches are used up (all matches occur)

    # Could this be done better? Absolutely. Do I have the patience to fix it? No.

    while match_list:

        # Creates an empty numpy array for this convention's schedule
        schedule = np.empty((num_days,games_per_day,2),dtype='object')

        # Create all matches
        match_list = list(combinations(convention,2))

        # Shuffle the matches
        shuffle(match_list)

        for nday, day in enumerate(schedule):

            schedule[nday,0] = match_list.pop()

            for ngame in range(games_per_day - 1):

                for idx, match in enumerate(match_list):
                    
                    if match[0] in day or match[1] in day:

                        continue 

                    else:

                        schedule[nday,ngame+1] = match_list.pop(idx)

                        break

    return schedule 
