"""
@created 04/11/2023 - 16:08

@author chris
"""

import pandas
import pandas as pd
from bs4 import BeautifulSoup

from utility.all_coaches_obj import Teams
from utility.coach_class import Coach

draft_teams = None


def html_from_excel(file_name):
    df = pd.read_excel(file_name)
    df: pandas.DataFrame
    df = df.dropna(how='all')
    return df.to_html()


def get_team_and_pkm_from_html(bs):
    bs_length = bs.select_one('tbody')
    bs = bs.select_one('tbody')
    draft_teams = Teams()
    conference_distance = 0
    conference_name = None
    for count in range(1, len(bs_length)):
        tag = bs.select_one('tr:nth-of-type(' + str(count) + ')')
        if tag is None:
            break
        p_team = None
        skipped_name = False
        for index in range(1, tag.__sizeof__()):
            hold = tag.select_one('td:nth-of-type(' + str(index) + ')')
            if hold is None:
                break
            elif hold.get_text() == 'NaN':
                pass
            elif 'Conference' in str(hold) or 'Test Draft' in str(hold):
                conference_distance = 2
                conference_name = hold.get_text()
            elif not conference_distance == 0:
                pass
            elif p_team is not None:
                if not skipped_name:
                    skipped_name = True
                    pass
                else:
                    p_team.add_pokemon(hold.get_text())
            elif conference_name is not None:
                p_team = Coach(hold.get_text(), conference_name)
                draft_teams.add_team(p_team)

        if conference_distance > 0:
            conference_distance -= 1
    return draft_teams


def init(file_name):
    teams_html = html_from_excel(file_name)
    bs = BeautifulSoup(teams_html, features="html.parser")
    return get_team_and_pkm_from_html(bs)
