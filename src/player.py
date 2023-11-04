__Author__ = "Luc Elliott"
__Version__ = "1.0.0"

from .pokemon import PokeMon
from .errors import PokemonError, PlayerError
from .constants import TERRAIN_MOVES


class Player:
    def __init__(self, player_id) -> None:
        self.pokemon = {}
        self.__player_id = player_id
        self.__terrain = {}

    def __repr__(self) -> str:
        pokemon_names = "\n" + "\n".join(self.pokemon.keys())
        return f"Player {self.__player_id} with pokemon: {pokemon_names}"
    
    @property
    def terrain(self):
        return self.__terrain

    def add_pokemon(self, pokemon):
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
        return self.__player_id

    def terrain_move(self, move, pokemon_name):
        if move not in TERRAIN_MOVES:
            raise PlayerError(f"Invalid terrain move {move}")
        if pokemon_name not in self.pokemon:
            raise PlayerError(f"Invalid pokemon {pokemon_name}")
        
        self.__terrain[move] = self.pokemon[pokemon_name]
        

        

