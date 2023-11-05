__Author__ = "Luc Elliott"
__Version__ = "1.0.0"

from .pokemon import PokeMon
from .errors import PokemonError, PlayerError
from .constants import TERRAIN_MOVES


class Player:
    """Class to represent a player

    Args:
        player_id (str): The id of the player, either p1 or p2
    
    Attributes:
        pokemon (dict): The pokemon the player has
        terrain (dict): The terrain moves the player has used
        player_id (str): The id of the player, either p1 or p2
    """

    def __init__(self, player_id) -> None:
        self.pokemon = {}
        self.__player_id = player_id
        self.__terrain = {}

    def __repr__(self) -> str:
        pokemon_names = "\n" + "\n".join(self.pokemon.keys())
        return f"Player {self.__player_id} with pokemon: {pokemon_names}"
    
    @property
    def terrain(self):
        """The terrain moves the player has used"""
        return self.__terrain

    def add_pokemon(self, pokemon: PokeMon) -> None:
        """Add a pokemon to the player

        Args:
            pokemon (PokeMon): The pokemon to add to the player

        Raises:
            PokemonError: If the pokemon is not a PokeMon instance
            PokemonError: If the pokemon name is None
            PokemonError: If the pokemon name already exists
        """

        if not isinstance(pokemon, PokeMon):
            raise PokemonError(f"Invalid pokemon {pokemon}")

        if pokemon.name is None:
            raise PokemonError("Pokemon name cannot be None")

        if pokemon.name in self.pokemon:
            print(f"Pokemon {pokemon.name} already exists" "adding _2 to name")
            pokemon.name = f"{pokemon.name}_2"

        self.pokemon[pokemon.name] = pokemon

    @property
    def player_id(self):
        """The id of the player, either p1 or p2"""
        return self.__player_id

    def terrain_move(self, move: str, pokemon_name: str) -> None:
        """Add a terrain move to the player

        Args:
            move (str): The name of the terrain move
            pokemon_name (str): The name of the pokemon that used the terrain 
            move

        Raises:
            PlayerError: If the move is not a terrain move
            PlayerError: If the pokemon name is not in the player's pokemon
        """

        if move not in TERRAIN_MOVES:
            raise PlayerError(f"Invalid terrain move {move}")
        if pokemon_name not in self.pokemon:
            raise PlayerError(f"Invalid pokemon {pokemon_name}")
        
        self.__terrain[move] = self.pokemon[pokemon_name]
        

        

