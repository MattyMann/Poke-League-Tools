"""
@created 04/11/2023 - 16:08

@author chris
"""

from utility.coach_class import Coach
import random


class Teams:
    def __init__(self):
        self.teams = list()
        self.pokemon = list()

    def add_team(self, given_team: Coach):
        self.teams.append(given_team)

    def get_all_coaches(self):
        return self.teams

    def get_coach_by_index(self, index: int):
        if self.teams[index] is not None:
            return self.teams[index]
        else:
            return None

    def get_coach_from_pkm(self, pokemon_list: list):
        correct_coach = None
        for team in self.teams:
            if correct_coach is None:
                correct_coach = team
            team: Coach
            for pokemon in team.get_pokemon():
                if pokemon in pokemon_list:
                    team.increase_likeliness()
            if team.likeliness > correct_coach.likeliness:
                correct_coach = team
        correct_coach.likeliness = 0
        return correct_coach

    def debug_get_rnd_team_pkm(self, rnd_ints):
        rnd_team = self.teams[random.randint(0, (len(self.teams) - 1))]
        rnd_pokemon = list()
        rnd_team: Coach
        for rnd_int in rnd_ints:
            rnd_pokemon.append(rnd_team.get_pokemon_by_pos(rnd_int))
        return rnd_pokemon, rnd_team
