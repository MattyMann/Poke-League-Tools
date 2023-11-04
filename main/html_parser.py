import re
from ast import literal_eval
import os
import argparse
from bs4 import BeautifulSoup
import pandas as pd
from elo_calc import elo_calc

p1_string = '|poke|p1'
p2_string = '|poke|p2'

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


def parse_html_file(file):
    soup = BeautifulSoup(file, features="html.parser")
    return _get_pokemon(soup)
    # Get players
    # This isn't a great solution as if Showdown change the format of names, this will fail
    # players = list(map(lambda i: i.string, soup.find_all(class_="subtle")))

    # Battle info
    battle_log = soup.find('script', class_='battle-log-data').string

    # print(output)

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
