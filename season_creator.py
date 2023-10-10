import math
import random
from itertools import combinations
import more_itertools
from random import shuffle
import pandas as pd
import numpy as np
import argparse
import os

season_num = 1

#CoachDsicords can be a 1 column csv of the coaches in this season, 
#it will search the coachdata.csv for relevant info 
 
Numweeks = 8
NumPlayoffs = 4


def create_conferences(CoachDiscords):

    #load in coachdata, shuffle, and remake into a pd dataframe
    Coaches = pd.read_csv(CoachDiscords)
    Coaches = Coaches.values.tolist()
    random.shuffle(Coaches)
    Coaches = pd.DataFrame(Coaches)
    print(Coaches)
    NumCoaches = len(Coaches)
    
    
    
    # sets the number of conferences must be a nicer way of doing this logic, this works for up to 30 players
    NumConfs = 0
    if NumCoaches < 16:
        NumConfs = 1
    elif NumCoaches % 3 == 0 & NumCoaches % 2 == 0:
        NumConfs = 3
    elif NumCoaches % 2 == 0:
        NumConfs = 2
    else: 
        NumConfs = 1        
    
    
    # Conference names, based on Jack's twisted preferences
    convnames = ['space','sky','shore']
       
    # Create a list of conventions based on elo
    conferences = dict(zip(convnames,map(lambda conv: conv.values.tolist(),np.split(Coaches,NumConfs))))
            
    # Make into lists
    for (name,conference) in conferences.items():
        
        conferences[name] = list(map(lambda player: player[0],conference))
        
    return conferences

#create the league tables 
def create_league_tables(conferences: dict):
    os.mkdir(r'C:\Users\matth\OneDrive\Documents\Github\Poke-League-Tools\season_'+str(season_num))
    for (name,conference) in conferences.items():
        table = pd.DataFrame({'team': conference})

        table['played'],table['wins'],table['losses'],table['draws'],table['points'],table['KOs'],table['faints'],table['k/d'] = 0,0,0,0,0,0,0,0
        # This should work but is causing issues. It might be more efficient if we can get it to work.
        # table = table.reindex(columns=['wins','losses','draws','points','kills','faints','k/d'], fill_value=0)

        table = table.astype({'team': 'string', 'wins': 'int8', 'losses': 'int8', 'draws': 'int8','points':'int8','KOs': 'int8', 'faints':'int8', 'k/d': 'int8'})

        table = table.sort_values(['points','k/d','wins'])
        os.mkdir(r'C:\Users\matth\OneDrive\Documents\Github\Poke-League-Tools\season_'+str(season_num)+'\conference'+name)
        table.to_csv(r'C:\Users\matth\OneDrive\Documents\Github\Poke-League-Tools\season_'+str(season_num)+'\conference'+name+'/table.csv', index=False)

    with open(r'C:\Users\matth\OneDrive\Documents\Github\Poke-League-Tools\season_'+str(season_num)+'\conference_'+name+'\table.csv', 'w') as f:
        f.write(str(conferences))
        f.close()

def create_matches(NumWeeks, NumPlayoffs, conference: list  ) -> list:
teams = [] #forogt which variable stores teams
if len(teams) % 2:
    teams.append('Day off')
n = len(teams)
matchs = []
fixtures = []
return_matchs = []
for fixture in range(1, n):
    for i in range(n/2):
        matchs.append((teams[i], teams[n - 1 - i]))
        return_matchs.append((teams[n - 1 - i], teams[i]))
    teams.insert(1, teams.pop())
    fixtures.insert(len(fixtures)/2, matchs)
    fixtures.append(return_matchs)
    matchs = []
    return_matchs = []

for fixture in fixtures:
    print fixture
    return schedule 

#testing 
life = create_conferences(r"C:\Users\matth\OneDrive\Documents\abc.csv")
rebirth = create_matches(8,4,life)
print(rebirth)