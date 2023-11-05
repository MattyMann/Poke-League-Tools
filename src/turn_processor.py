__Author__ = "Luc Elliott"
__Version__ = "1.0.0"

import src.constants as const
from .player import Player 
from .pokemon import PokeMon
from .errors import PokemonError
from typing import Union, Tuple


class TinaTurner:
    """
    Class to process turns in a Pokemon battle, and update the player objects

    Args:
        turns (list): A list of turns in a Pokemon battle
        **kwargs: Keyword arguments to pass to the class

    Attributes:
        players (dict): The players in the battle
        turns (list): A list of turns in a Pokemon battle
        attack_defender (tuple): The pokemon that is attacking and the pokemon
         that is being attacked
    
        
    """
    def __init__(self, turns, **kwargs) -> None:
        player1 = kwargs.get("player1")
        player2 = kwargs.get("player2")
        self.players = {"p1": player1, "p2": player2}
        self.turns = turns
        self.attack_defender = None
        self.run()

    def run(self):
        """Runs the turn processor
        
        Returns:
            None
            
        Note:
            Need to add in healing and activated moves 
            These will be keep a more accurate track of the pokemon's health

        """
        for turn in self.turns:
            player_info = self.extract_player_info(turn)
            if player_info is None:
                continue
            player = self.players.get(player_info)

            if turn.startswith("|-damage|"):
                player = self.hurt_or_dead(turn, player)

            elif turn.startswith("|move|"):
                self.find_attack_defender(turn)
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

    def other_player(self, player: Player):
        """
        Finds the other player in the battle
        
        Args:
            player (Player): The player object whose move is being processed
        
        Returns:
            Player: The other player in the battle
        """
        values = list(self.players.values())
        return values[0] if values[0] != player else values[1]

    def status_setter(self, turn: str, player: Player) -> None:
        """
        Sets the status condition of the pokemon
        
        Args:
            turn (str): The current turn being processed
            player (Player): The player object whose move is being processed
            
        Returns:
            None"""
        status = turn.split("|")[3]
        other_player = self.other_player(player)
        if status not in const.STATUS_CONDITIONS:
            print("Status condition not found")

        if self.attack_defender:
            afflicted_pokemon = player.pokemon[self.attack_defender[1]]
            status_causer = other_player.pokemon[self.attack_defender[0]]
            afflicted_pokemon.status = status
            afflicted_pokemon.status_causer = status_causer

    def hurt_or_dead(self, turn: str, player: Player) -> Player:
        if const.DAMAGE.search(turn):
            damage = const.DAMAGE.search(turn).group()[:-5]

            if any([status in turn for status in const.STATUS_CONDITIONS]):
                self.status_damage(turn, player, damage)
                
            elif self.attack_defender:
                self.attack_damage(player, damage)
            else:
                self.misc_damage(turn, player, damage)

        elif const.FAINT.search(turn):
            self.fainted(turn, player)
        
        # resets the attack reciever
        self.attack_defender = None
        return player
    
    def terrain_check(self, turn: str, player: Player) -> None:
        """Checks if the move used triggers a terrain move.
        The terrain move and the activating pokemon are saved to the player.
        This is used to track kills due to terrain.
        

        Args:
            turn (str): The current turn being processed.
            player (Player): The player object whose move is being processed.

        Returns:
            None

        Note:
            This just reads if a terrain move has been activated, 
        """
        if turn.split("|")[3] in const.TERRAIN_MOVES:
            player.terrain_move(turn.split("|")[3], self.attack_defender[0])

    @staticmethod
    def find_current_pokemon(turn: str) -> str:
        """Finds the current pokemon in a turn.

        Args:
            turn (str): A string representing a turn in a Pokemon battle.

        Returns:
            str: The name of the current pokemon.
        """

        pokemons = const.POKEMON_SEARCH.findall(turn)
        if pokemons and len(pokemons) == 1:
            return pokemons[0].split(": ")[1]
        
        else:
            return None

    def find_attack_defender(self, turn: str) -> Union[None, tuple]:
        """Finds the pokemon that is attacking and the pokemon that is being 
        attacked.

        Args:
            turn (str): A string representing a turn in a Pokemon battle.

        """

        pokemons = const.POKEMON_SEARCH.findall(turn)
        if pokemons and len(pokemons) == 2:
            if pokemons[0] == pokemons[1]:
                return None
            self.attack_defender = (pokemons[0].split(": ")[1],
                                    pokemons[1].split(": ")[1])

    def extract_player_info(self, turn) -> Union[str, None]:
        # Extracts the player information from the turn
        
        turn = "|".join(turn.split("|")[:3])
        if const.PLAYER_SEARCH.search(turn):
            return const.PLAYER_SEARCH.search(turn).group()[:-1]
        else:
            return None
        
    def return_players(self) -> Tuple[Player, Player]:

        return self.players["p1"], self.players["p2"]
    
    def heal(self, turn, player):
        # Need to finish
        pass

    def status_damage(self, turn, player, damage):
        """Processes damage from a status condition

        Args:
            turn (str): The current turn being processed
            player (Player): The player object whose move is being processed
            damage (str): The damage dealt to the pokemon
        """
        pokemon = self.find_current_pokemon(turn)
        player.pokemon[pokemon].hp = int(damage)

    def attack_damage(self, player, damage):
        """Processes damage from an attack
        
        Args:
            player (Player): The player object whose move is being processed
            damage (str): The damage dealt to the pokemon"""
        player.pokemon[self.attack_defender[1]].hp = int(damage)

    def misc_damage(self, turn, player, damage):
        """Processes damage that is not from an attack or status condition
        
        Args:
            turn (str): The current turn being processed
            player (Player): The player object whose move is being processed
            damage (str): The damage dealt to the pokemon
        """

        pokemon = self.find_current_pokemon(turn)
        player.pokemon[pokemon].hp = int(damage)

    def fainted(self, turn, player):
        defender = player
        attacker = self.other_player(player)
        
        if any([status in turn for status in const.STATUS_CONDITIONS]):
            # Find deaths due to status conditions
            pokemon = self.find_current_pokemon(turn)
            self.kill_counter(
                defender.pokemon[pokemon], 
                defender.pokemon[pokemon].status_causer)
        
        elif any([terrain in turn for terrain in const.TERRAIN_MOVES]):
            # Deaths due to terrain
            move_index = [terrain in turn for 
                          terrain in const.TERRAIN_MOVES].index(True)
            move = const.TERRAIN_MOVES[move_index]
            pokemon = self.find_current_pokemon(turn)

            self.kill_counter(
                defender.pokemon[pokemon], attacker.terrain[move])
            
        elif self.attack_defender:
            # Deaths due to attacks
            if self.attack_defender[0] in player.pokemon:
                fainted_pokemon, killer = (self.attack_defender[0],
                                           self.attack_defender[1])
                
            elif self.attack_defender[1] in player.pokemon:
                fainted_pokemon, killer = (self.attack_defender[1],
                                           self.attack_defender[0])
            
            self.kill_counter(
                defender.pokemon[fainted_pokemon],
                attacker.pokemon[killer])
            
    def kill_counter(self, killed, killer):
        """Updates the kill count for the pokemon that killed another pokemon
        
        Args:
            killed (PokeMon): The pokemon that was killed
            killer (PokeMon): The pokemon that killed the other pokemon
        
        Raises:
            PokemonError: If the killed or killer is not a PokeMon instance"""
        
        if not isinstance(killed, PokeMon):
            raise PokemonError(f"Invalid killed {killed}")
        if not isinstance(killer, PokeMon):
            raise PokemonError(f"Invalid killer {killer}")
        
        killed.hp = 0
        killed.killed_by = killer
        killer.kills += 1
