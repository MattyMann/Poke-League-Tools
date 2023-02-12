import pandas as pd
import math
import numpy as np
from itertools import combinations

def conventions( rankings ) -> list:

    # Read in the ratings for elo calc
    ratings = pd.read_parquet(rankings)
    
    ratings = ratings.astype({'username': 'string', 'elo': 'int16', 'active': 'bool'}).sort_values('elo',ascending=False)
    
    # Create a new DF with just the active players
    active_players = ratings[ratings['active'] == True].drop(columns=['elo','active'])
    
    # How many conventions should be made? By default we say there should be eight per convention
    num_of_conventions = math.ceil(len(active_players) / 8)
    
    active_players = active_players.to_numpy()
    
    conventions = list(map(lambda conv: conv.tolist(),np.split(active_players,num_of_conventions)))

    for idx, convention in enumerate(conventions):
        
        conventions[idx] = list(map(lambda player: player[0],convention))
        
    return conventions

def matches( convention: list):

    num_players = len(convention)

    if num_players % 2:
        convention.append('Day Off')
        num_players += 1

    match_list = list(combinations(convention,2))

    num_days = num_players - 1

    games_per_day = num_players // 2

    schedule = np.empty((num_days,games_per_day,2),dtype='object')

    while match_list != []:

        for nday, day in enumerate(schedule):
            
            if match_list == []:
                break
            
            else:
                t_val = sum(map(lambda player: True if player in day else False, match_list[-1]))

                if t_val != 0:

                    pass 

                else:

                    for ngame, game in enumerate(day):

                        if game.all() == None:
                        
                            schedule[nday,ngame] = match_list.pop()

                            break

    print(schedule)

conv = conventions("data/rankings.pq")

for i in conv:
    matches(i)
