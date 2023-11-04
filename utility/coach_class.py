"""
@created 04/11/2023 - 16:08
   
@author chris
"""


class Coach:
    def __init__(self, team_name, conference):
        self.team_name = team_name
        self.conference = conference
        self.pokemon = list()
        self.likeliness = 0

    def add_pokemon(self, pokemon):
        self.pokemon.append(pokemon)

    def get_pokemon(self):
        return self.pokemon

    def get_pokemon_by_pos(self, pos: int):
        list_length = len(self.pokemon) - 1
        if pos <= list_length:
            return self.pokemon[pos]

    def get_team_name(self):
        return self.team_name

    def get_team_and_pokemon(self):
        list_to_return = self.pokemon
        list_to_return.insert(0, self.team_name)
        return list_to_return

    def increase_likeliness(self):
        self.likeliness += 1

    def reset_likeliness(self):
        self.likeliness = 0
