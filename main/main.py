"""
@created 04/11/2023 - 16:08

@author chris
"""

from bot import run_discord_bot
from debug.rnd_pkm_picker import get_random_ints, get_20_rnd_ints


def debug_check_pokemon(given_teams):
    rnd_ints = get_random_ints()
    rnd_pokemon, correct_team = given_teams.debug_get_rnd_team_pkm(rnd_ints)

    if correct_team == given_teams.get_coach_from_pkm(rnd_pokemon):
        print('Correct team picked!')
        print('Pokemon were: ' + str(rnd_pokemon))
        print('So the team is: ' + str(correct_team.get_team_name()))


if __name__ == "__main__":
    run_discord_bot()
