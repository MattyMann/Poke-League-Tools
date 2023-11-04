import re
from bs4 import BeautifulSoup
import pandas as pd
from elo_calc import elo_calc
from init_teams import init
#from season_creator import create_conventions
from utility.coach_class import Coach

p1_string = '|poke|p1'
p2_string = '|poke|p2'
exel_doc_name = 'D:\Python\Poke-League-Tools-main\MPCL NatDex Test Draft (1).xlsx'


def _get_pokemon(parser: BeautifulSoup):
    user_one_pokemon = list()
    user_two_pokemon = list()
    output = parser.find('script', class_='battle-log-data').get_text()
    for idx, row in enumerate(output.splitlines()):
        if idx < 10:
            continue
        elif p1_string in row:
            start_index = (len(p1_string) + 1)
            if ', ' in row:
                end_index = row.index(',')
                user_one_pokemon.append(row[start_index:end_index])
            else:
                user_one_pokemon.append(row[start_index:(len(row) - 1)])
        elif p2_string in row:
            start_index = (len(p2_string) + 1)
            if ', ' in row:
                end_index = row.index(',')
                user_two_pokemon.append(row[start_index:end_index])
            else:
                user_two_pokemon.append(row[start_index:(len(row) - 1)])

        if idx > 50:
            break

    return user_one_pokemon, user_two_pokemon


def get_both_player(parser, draft_teams):
    team_name_list = list()
    p1_pokemon, p2_pokemon = _get_pokemon(parser)
    print(p1_pokemon)
    print(p2_pokemon)
    # print(draft_teams.get_all_teams())
    # print(draft_teams.get_team_from_pkm(p1_pokemon))
    team1_obj = draft_teams.get_coach_from_pkm(p1_pokemon)

    team1_obj: Coach
    team2_obj = draft_teams.get_coach_from_pkm(p2_pokemon)
    team2_obj: Coach
    if team1_obj is not None:
        team_name_list.append(team1_obj.get_team_name())
    else:
        print('Team1 object is null')
    if team2_obj is not None:
        team_name_list.append(team2_obj.get_team_name())
    else:
        print('Team2 object is null')
    return team_name_list


def summary_data(file):  # -> dict:
    """
    Extracts the relevant information from an HTML battle file
    --------------
    Input
    -----
    file: the HTML file containing the battle

    Output
    ------
    summary (dict): a dict containing the key information about the battle
    """

    # Parse html file
    # print(file)
    soup = BeautifulSoup(file, features="html.parser")

    # Get players
    # This isn't a great solution as if Showdown change the format of names, this will fail
    # players = list(map(lambda i: i.string, soup.find_all(class_="subtle")))
    draft_teams = init(exel_doc_name)
    players = get_both_player(soup, draft_teams)

    # Battle info
    battle_log = soup.find('script', class_='battle-log-data').string

    # Find any mention of the tie tag, |tie
    tie = re.search('\|tie\n', battle_log)

    # Find the number of faints for each player
    user_one_faints = len(re.findall('\|faint\|p1a', battle_log))
    user_two_faints = len(re.findall('\|faint\|p2a', battle_log))

    # How to account for revival blessing
    revival_count_p1 = len(re.findall('Revival Blessing\|p1a', battle_log))
    revival_count_p2 = len(re.findall('Revival Blessing\|p2a', battle_log))

    # times
    times = re.findall('(?<=\|t:\|)(?>.+)', battle_log)

    # turns
    turns = len(re.findall('(?<=\|turn\|)(?>.+)', battle_log))

    # Check if a draw occurred. If not, declare a winner
    winner = None
    if tie is None:

        winner = re.search('(?<=\|win\|)(?>.+)', battle_log).group(0)

        draw = False

    else:

        draw = True

    # summary is the dict that we eventually return. It contains the..., well, summary information about the match.
    summary = {
        "player_one": players[0],  # str
        "player_two": players[1],  # str
        "n_faint_one": user_one_faints - revival_count_p1,  # int
        "n_faint_two": user_two_faints - revival_count_p2,  # int
        "win_draw_status": 0 if draw else (1 if winner == players[0] else 2),  # int
        "start_time": int(times[0]),  # int
        # just for analysis
        "end_time": int(times[-1]),  # int
        "n_rounds": turns  # int
    }

    return summary


def update_elos(BattleInfo: dict):
    """
    Updates the elos in the permanent rankings file, data/rankings.pq
    -----------
    BattleInfo: a dict of the summary info from the summary_data 
    -----------
    """

    # Read the ratings
    rankings = pd.read_parquet("data/rankings.pq")

    # Check if users exists. If not, initialise and add them
    for num in ["one", "two"]:
        while 1:
            if rankings.loc[rankings['username'] == BattleInfo['player_' + num]].empty:
                idx = input(BattleInfo[
                                'player_' + num] + " doesn't exist! Is this an alias for another player? (player_idx/n): ")
                if idx == "n":
                    rankings.loc[len(rankings)] = [BattleInfo['player_' + num], 1000]
                    break
                elif type(idx) == int:
                    print(rankings['username'])
                    confirmation = input(
                        "You have chosen " + rankings.loc[idx]['username'] + ". Is this correct? (y/n)")
                    if confirmation == "y":
                        rankings.loc[idx]['username'] = BattleInfo['player_' + num]
                        break
                    elif confirmation == "n":
                        continue
                else:
                    print("Invalid input! Please choose a valid option")
                    continue
            else:
                break

    # Get current elos
    player_one_elo = rankings[rankings['username'] == BattleInfo['player_one']]['elo'].values[0]

    player_two_elo = rankings[rankings['username'] == BattleInfo['player_two']]['elo'].values[0]

    # The k_val of the game
    # It scales with kill difference in the game, K = 16*(1 + d/6) where d is the difference. Therefore in a perfect sweep, d=6 and K=32; a pyrrhic victory would be d=3 and K=24; and scraping a win would be d=0 and K=16.
    k_val = 16 * (1 + (abs(BattleInfo['n_faint_one'] - BattleInfo['n_faint_two']) / 6))

    # Calc new elos
    new_elo_one = elo_calc(player_one_elo, player_two_elo, 0.5 if BattleInfo['win_draw_status'] == 0 else (
        1 if BattleInfo['win_draw_status'] == 1 else 0), k_val)

    new_elo_two = elo_calc(player_two_elo, player_one_elo, 0.5 if BattleInfo['win_draw_status'] == 0 else (
        1 if BattleInfo['win_draw_status'] == 2 else 0), k_val)

    # Set new elo
    rankings.loc[(rankings['username'] == BattleInfo['player_one']), 'elo'] = new_elo_one

    rankings.loc[(rankings['username'] == BattleInfo['player_two']), 'elo'] = new_elo_two

    # Need this to correct for Python not handling 16 bit ints
    rankings = rankings.astype({'elo': 'int16'})

    # Write rankings back to file
    rankings.to_parquet("data/rankings.pq")

# def update_table(file, season_num: int):
#
#    battleInfo = summary_data(file)
#
#    with open("seasons/season"+str(season_num)+"/index") as indexfile:
#
#        index = literal_eval(indexfile.read())
#        
#        for (name, convention) in index.items():
#            if battleInfo['player_one'] in convention and battleInfo['player_two'] in convention:
#                rel_league = name
#            else:
#                continue
#
#        try:
#            rel_league
#        except:
#            raise Exception(battleInfo['player_one'] + " and " + battleInfo['player_two'] + " are not in the same league")
#
#        table_file = "seasons/season"+str(season_num)+"/table_"+rel_league
#
#        if os.path.isfile(table_file):
#
#            table = pd.read_parquet(table_file)
#        else:
#            table = pd.DataFrame(columns=['username','wins', 'losses', 'draws','points','kills', 'faints', 'k/d'])
#
#            table = table.astype({'username': 'string', 'wins': 'int8', 'losses': 'int8', 'draws': 'int8','points':'int8','kills': 'int8', 'faints':'int8', 'k/d': 'int8'})
#
#        if battleInfo['win_draw_status'] == 0:
#            table.loc[table['username'] == battleInfo['player_one'],'draws'] += 1
#            table.loc[table['username'] == battleInfo['player_two'],'draws'] += 1
#            table.loc[table['username'] == battleInfo['player_one'],'points'] += 1
#            table.loc[table['username'] == battleInfo['player_two'],'points'] += 1
#        elif battleInfo['win_draw_status'] ==  1:
#            table.loc[table['username'] == battleInfo['player_one'],'wins'] += 1
#            table.loc[table['username'] == battleInfo['player_two'],'losses'] += 1
#            table.loc[table['username'] == battleInfo['player_one'],'points'] += 3
#            table.loc[table['username'] == battleInfo['player_two'],'points'] += 0
#        elif battleInfo['win_draw_status'] == 2:
#            table.loc[table['username'] == battleInfo['player_one'],'losses'] += 1
#            table.loc[table['username'] == battleInfo['player_two'],'wins'] += 1
#            table.loc[table['username'] == battleInfo['player_one'],'points'] += 0
#            table.loc[table['username'] == battleInfo['player_two'],'points'] += 3
#
#        table.loc[table['username'] == battleInfo['player_one'],'kills'] += battleInfo['n_faint_two']
#
#        table.loc[table['username'] == battleInfo['player_two'],'kills'] += battleInfo['n_faint_one']
#
#        table.loc[table['username'] == battleInfo['player_one'],'faints'] += battleInfo['n_faint_one']
#
#        table.loc[table['username'] == battleInfo['player_two'],'faints'] += battleInfo['n_faint_two']
#
#        table.loc[table['username'] == battleInfo['player_one'],'k/d'] = table.loc[table['username'] == battleInfo['player_one'],'kills'] - table.loc[table['username'] == battleInfo['player_one'],'faints'] 
#
#        table.loc[table['username'] == battleInfo['player_two'],'k/d'] = table.loc[table['username'] == battleInfo['player_two'],'kills'] - table.loc[table['username'] == battleInfo['player_two'],'faints'] 
#
#        table.sort_values(by=['points','k/d','kills','faints'],ascending=[False,False,True],inplace=True)
#
#        table.to_parquet(table_file)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('html_file')
#
#     args = parser.parse_args()
#
#     with open(args.html_file) as file:
#         summary = summary_date(file)
#         update_elos(summary)
