import pandas as pd
import math
import numpy as np

def conventions( rankings ) -> list:

    # Read in the ratings for elo calc
    ratings = pd.read_parquet(rankings)
    
    ratings = ratings.astype({'username': 'string', 'elo': 'int16', 'active': 'bool'}).sort_values('elo',ascending=False)
    
    active_players = ratings[ratings['active'] == True].drop(columns=['elo','active'])
    
    num_of_conventions = math.ceil(len(active_players) / 8)
    
    active_players = active_players.to_numpy()
    
    conventions = list(map(lambda conv: conv.tolist(),np.split(active_players,num_of_conventions)))

    for idx, convention in enumerate(conventions):
        
        conventions[idx] = list(map(lambda player: player[0],convention))
        
    return conventions
