import pandas as pd
import time
import os 

# creates an empty pd dataframe for coachdata
CoachData = pd.DataFrame(columns=['name', 'discord', 'team', 'showdown', 'elo',
                                  'seasons played', 'games played', 'wins',
                                  'losses', 'draws', 'KOs', 'faints', 'K/D'])
Players = {}

#creates a callable class for coach data
class Createcoach:
    def __init__(self, name, discord, team, showdown):
        self.name, self.discord, self.team, self.showdown = name, discord, team, showdown
        self.elo, self.seasons_played, self.games_played, self.wins, self.losses, self.draws, self.KOs, self.faints, self.k_d  = 1000, 0, 0, 0, 0, 0, 0, 0, 0


#creates a new index player in Players and uses the Createcoach constructor to add 
#their data into the dataframe
async def Add_player(ctx, name, discord, team, showdown):
    global CoachData
    Players['Player'+str(len(CoachData))] = 'a'
    cp = Players['Player'+str(len(CoachData))]
    cp = Createcoach(name, discord, team, showdown)
    CoachDataList = [cp.name, cp.discord, cp.team,
                     cp.showdown, cp.elo, cp.seasons_played,
                     cp.games_played, cp.wins, cp.losses, cp.draws, cp.KOs,
                     cp.faints, cp.k_d]
    CoachData = pd.concat([CoachData, pd.DataFrame([CoachDataList], columns=CoachData.columns)])
    #deletes the old file, then creates a new one with the updated data
    time.sleep(1)
    os.remove(r'C:\Users\matth\OneDrive\Documents\GitHub\Poke-League-Tools\CoachData.csv')
    CoachData.to_csv(r'C:\Users\matth\OneDrive\Documents\GitHub\Poke-League-Tools\CoachData.csv')
    #note the first row of the csv is the column headings
    
    
print(CoachData)    
        