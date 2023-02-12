from bs4 import BeautifulSoup
import re
import argparse
from elo_calc import elo_calc
import pandas as pd

# Parser for html file
parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('-d',action="store_true")
parser.add_argument('-q',action="store_true")

args = parser.parse_args()

def battle_info(file) -> dict:
    
    soup = BeautifulSoup(file, features="html.parser")

    # Get players
    title = soup.title.string

    players = list(map(lambda i: i.string, soup.find_all(class_="subtle"))) # This is not a great solution if Showdown change the format of the page

    # Battle info

    battle_log = soup.find('script',class_='battle-log-data').string

    # Find any mention of the tie tag, |tie
    tie = re.search('\|tie\n',battle_log)

    # Find the number of faints for each player
    user_one_faints = len(re.findall('\|faint\|p1a',battle_log))

    user_two_faints = len(re.findall('\|faint\|p2a',battle_log))

    # Check if a draw occurred. If not, declare a winner
    if tie == None:

        winner = re.search('(?<=\|win\|)(?>.+)',battle_log).group(0)
        
        draw = False

    else:

        draw = True

    summary = {"player_one": players[0],
            "player_two": players[1],
            "n_faint_one": user_one_faints,
            "n_faint_two": user_two_faints,
            "win_draw_status": draw if draw else winner}

    if not bool(args.q):
        print(summary['player_one'] + " vs. " + summary['player_two'] + "\n" + str(summary['n_faint_one']) + " - " + str(summary['n_faint_two']) + "\n" + ("draw" if summary['win_draw_status'] == True else summary['win_draw_status'])  + "\nDoes this look correct (y/n)?")
    
        answer = input()

        if answer == "y":
            return summary
        else:
            raise Exception()
    else:
        return summary

def update_elos( file ):

    with open(file) as f:
        
        # Get the battle info
        battleInfo = battle_info(f)

        # Read the ratings
        ratings = pd.read_parquet("data/rankings.pq")

        # Parse the datatypes for efficiency
        ratings = ratings.astype({'username': 'string', 'elo':'int16', 'active': 'bool'})

        # Check if users exists. If not, initialise and add them
        if ratings.loc[ratings['username'] == battleInfo['player_one']].empty: 
            ratings.loc[len(ratings)] = [battleInfo['player_one'],1000]
        if ratings.loc[ratings['username'] == battleInfo['player_two']].empty:
            ratings.loc[len(ratings)] = [battleInfo['player_two'],1000]

        # Get current elos
        player_one_elo = ratings[ratings['username'] == battleInfo['player_one']]['elo'].values[0]

        player_two_elo = ratings[ratings['username'] == battleInfo['player_two']]['elo'].values[0]

        # The k_val of the game
        k_val = 32 * (1 + (abs(battleInfo['n_faint_one'] - battleInfo['n_faint_two'])/6))

        # Calc new elos
        new_elo_one = elo_calc(player_one_elo,player_two_elo,0.5 if battleInfo['win_draw_status'] == True else ( 1 if battleInfo['player_one'] == battleInfo['win_draw_status'] else 0 ), k_val)

        new_elo_two = elo_calc(player_two_elo,player_one_elo,0.5 if battleInfo['win_draw_status'] == True else ( 1 if battleInfo['player_two'] == battleInfo['win_draw_status'] else 0 ), k_val)

        # Set new elo
        ratings.loc[(ratings['username'] == battleInfo['player_one']),'elo'] = new_elo_one

        ratings.loc[(ratings['username'] == battleInfo['player_two']),'elo'] = new_elo_two

        # Output
        if bool(args.d):
            print(ratings)
        else:   
            ratings.to_parquet("data/rankings.pq")

def update_table(file,table_file):

    with open(file) as f:

        table = pd.read_parquet(table_file)

        table = table.astype({'username': 'string', 'wins': 'int8', 'losses': 'int8', 'draws': 'int8','points':'int8','kills': 'int8', 'faints':'int8', 'k/d': 'int8'})

        battleInfo = battle_info(file)

        match battleInfo['win_draw_status']:
            case True:
                table.loc[table['username'] == battleInfo['player_one'],'draws'] += 1
                table.loc[table['username'] == battleInfo['player_two'],'draws'] += 1
                table.loc[table['username'] == battleInfo['player_one'],'points'] += 1
                table.loc[table['username'] == battleInfo['player_two'],'points'] += 1
            case battleInfo['player_one']:
                table.loc[table['username'] == battleInfo['player_one'],'wins'] += 1
                table.loc[table['username'] == battleInfo['player_two'],'losses'] += 1
                table.loc[table['username'] == battleInfo['player_one'],'points'] += 3
                table.loc[table['username'] == battleInfo['player_two'],'points'] += 0
            case battleInfo['player_two']:
                table.loc[table['username'] == battleInfo['player_one'],'losses'] += 1
                table.loc[table['username'] == battleInfo['player_two'],'wins'] += 1
                table.loc[table['username'] == battleInfo['player_one'],'points'] += 0
                table.loc[table['username'] == battleInfo['player_two'],'points'] += 3

        print(table)

update_elos(str(args.filename)) 

