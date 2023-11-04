__Author__ = "Luc Elliott"
__Version__ = "1.0.0"

import re
from .constants import TERRAIN_MOVES, STATUS_CONDITIONS, FAINT, DAMAGE


class TinaTurner:
    def __init__(self, turns, **kwargs) -> None:
        player1 = kwargs.get("player1")
        player2 = kwargs.get("player2")

        self.players = {"p1": player1, "p2": player2}
        self.turns = turns
        self.attack_reciever = None
        self.current_pokemon = None

        self.run()

    def run(self):
        for turn in self.turns:
            player_info = self.extract_player_info(turn)
            if player_info is None:
                continue
            player = self.players.get(player_info)

            if turn.startswith("|-damage|"):
                player = self.damage(turn, player)

            elif turn.startswith("|move|"):
                self.find_pokemon(turn)
                self.terrain_check(turn, player)


            elif turn.startswith("|-status|"):
                self.status_setter(turn, player)

            # Need to add this back in, damage casued by status conditions
            # elif turn.startswith("|-activate|"):
            #     self.activate_setter(player)
                # this is for damage from status conditions

            elif turn.startswith("|-heal|"):
                self.heal(turn, player)

            self.players[player_info] = player

    def other_player(self, player):
        # find the player that isn't the main player for the turn
        values = list(self.players.values())
        return values[0] if values[0] != player else values[1]

    def status_setter(self, turn, player):
        status = turn.split("|")[3]
        other_player = self.other_player(player)
        if status not in STATUS_CONDITIONS:
            print("Status condition not found")
        if self.attack_reciever:
            afflicted_pokemon = player.pokemon[self.attack_reciever[1]]
            status_causer = other_player.pokemon[self.attack_reciever[0]]
            afflicted_pokemon.status = status
            afflicted_pokemon.status_causer = status_causer

    def damage(self, turn, player):
        if DAMAGE.search(turn):
            damage = DAMAGE.search(turn).group()[:-5]

            if any([status in turn for status in STATUS_CONDITIONS]):
                # Looks for damage in status conditions
                self.find_pokemon(turn)
                player.pokemon[self.current_pokemon].hp = int(damage)
            elif self.attack_reciever:
                # Looks for damage in attacks
                player.pokemon[self.attack_reciever[1]].hp = int(damage)
            else:
                self.find_pokemon(turn)
                player.pokemon[self.current_pokemon].hp = int(damage)

        elif FAINT.search(turn):
            # Kill tracking section
            defender = player
            attacker = self.other_player(player)
            
            if any([status in turn for status in STATUS_CONDITIONS]):
                # Find deaths due to status conditions
                self.find_pokemon(turn)
                defender.pokemon[self.current_pokemon].hp = 0
                defender.pokemon[self.current_pokemon].killed_by = defender.pokemon[self.current_pokemon].status_causer
                defender.pokemon[self.current_pokemon].status_causer.kills += 1
            
            elif any([terrain in turn for terrain in TERRAIN_MOVES]):
                # Deaths due to terrain
                move_index = [terrain in turn for terrain in TERRAIN_MOVES].index(True)
                move = TERRAIN_MOVES[move_index]
                self.find_pokemon(turn)
                defender.pokemon[self.current_pokemon].hp = 0
                defender.pokemon[self.current_pokemon].killed_by = attacker.terrain[move]
                attacker.terrain[move].kills += 1

            elif self.attack_reciever:
                # Deaths due to attacks
                
                if self.attack_reciever[0] in player.pokemon:
                    fainted_pokemon, killer = self.attack_reciever[0], self.attack_reciever[1]
                    
                elif self.attack_reciever[1] in player.pokemon:
                    fainted_pokemon, killer = self.attack_reciever[1], self.attack_reciever[0]
                
                attacker.pokemon[killer].kills += 1
                defender.pokemon[fainted_pokemon].killed_by = killer
                defender.pokemon[fainted_pokemon].hp = 0
        
        # resets the attack reciever
        self.attack_reciever = None
        return player

    # Finds if a terrain move has been activated
    def terrain_check(self, turn, player):
        if turn.split("|")[3] in TERRAIN_MOVES:
            player.terrain_move(turn.split("|")[3], self.attack_reciever[0])

    def find_pokemon(self, turn):
        # Finds the pokemon, if 2 pokemon are found, it is an attack
        # if 1 pokemon is found, it is a status move

        pokemon_search = re.compile(r"p[1-2]a: [A-Za-z0-9]+")
        pokemons = pokemon_search.findall(turn)
        if pokemons and len(pokemons) == 1:
            self.current_pokemon = pokemons[0].split(": ")[1]
        
        elif pokemons and len(pokemons) == 2:
            if pokemons[0] == pokemons[1]:
                return None
            
            self.attack_reciever = (
                pokemons[0].split(": ")[1],
                pokemons[1].split(": ")[1],
            )

    def extract_player_info(self, turn):
        # Extracts the player information from the turn
        player_search = re.compile(r"p[1-2]a")
        turn = "|".join(turn.split("|")[:3])
        if player_search.search(turn):
            return player_search.search(turn).group()[:-1]
        else:
            return None
        
    def return_players(self):
        return self.players["p1"], self.players["p2"]
    
    def heal(self, turn, player):
        # Need to finish
        pass
