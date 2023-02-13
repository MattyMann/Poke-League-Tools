import pandas as pd
import math
import numpy as np
from itertools import combinations
from random import shuffle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('season_num',type=int)

args = parser.parse_args()

def conventions( rankings ) -> list:

    # Read in the ratings for elo calc
    ratings = pd.read_parquet(rankings)
    
    ratings = ratings.astype({'username': 'string', 'elo': 'int16', 'active': 'bool'}).sort_values('elo',ascending=False)
    
    # Create a new DF with just the active players
    active_players = ratings[ratings['active'] == True].drop(columns=['elo','active'])
    
    # How many conventions should be made? By default we say there should be eight per convention
    num_of_conventions = math.ceil(len(active_players) / 8)
    
    # How many players are 'active', i.e., will be playing this season
    active_players = active_players.to_numpy()
    
    # Create a list of conventions based on elo
    conventions = list(map(lambda conv: conv.tolist(),np.split(active_players,num_of_conventions)))

    # Make into lists
    for idx, convention in enumerate(conventions):
        
        conventions[idx] = list(map(lambda player: player[0],convention))
        
    return conventions

def matches( convention: list ) -> list:

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

    while match_list != []:
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

def league_table( convention: list):

    table = pd.DataFrame({'username': convention})

    table['wins'],table['losses'],table['draws'],table['points'],table['kills'],table['faints'],table['k/d'] = 0,0,0,0,0,0,0
    
    table = table.astype({'username': 'string', 'wins': 'int8', 'losses': 'int8', 'draws': 'int8','points':'int8','kills': 'int8', 'faints':'int8', 'k/d': 'int8'})

    table = table.sort_values(['points','k/d'])

    return table

for idx, convention in enumerate(conventions("data/rankings.pq")):

    matches(convention)
    league = league_table(convention)
    league.to_parquet("seasons/season"+str(args.season_num)+"/table_" + str(idx))
