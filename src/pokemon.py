__Author__ = "Luc Elliott"
__Version__ = "1.0.0"

from .constants import STATUS_CONDITIONS
from .errors import PokemonError


class PokeMon:
    """Class to represent a pokemon
    
    Args:
        pokemon_name (str): The name of the pokemon
    
    Attributes:
        kills (int): The number of kills the pokemon has made
        killed_by (PokeMon): The pokemon that killed this pokemon
        status (str): The status condition of the pokemon
        status_causer (PokeMon): The pokemon that caused the status condition
        hp (int): The current hp of the pokemon
        name (str): The name of the pokemon

        """
    def __init__(self, pokemon_name) -> None:
        self.__kills = 0
        self.__killed_by = None
        self.__status = None
        self.__status_causer = None
        self.__hp = 100

        self.__name = pokemon_name

    def __repr__(self) -> str:

        return f"""
{self.name} with {self.hp} hp, Kills {self.kills}, 
Killed by {self.killed_by}"""

    @property
    def kills(self):
        """The number of kills the pokemon has made"""
        return self.__kills

    @kills.setter
    def kills(self, value):
        if not isinstance(value, int):
            raise PokemonError(f"Invalid kills {value}")
        
        self.__kills = value

    @property
    def killed_by(self):
        """The pokemon that killed this pokemon"""
        return self.__killed_by

    @killed_by.setter
    def killed_by(self, value):
        if not isinstance(value, PokeMon):
            raise PokemonError(f"Invalid killed by {value}")
        
        self.__killed_by = value

    @property
    def status(self):
        """The status condition of the pokemon"""
        return self.__status

    @status.setter
    def status(self, status):
        if status not in STATUS_CONDITIONS:
            raise ValueError(f"Invalid status condition {status}")
        self.__status = status

    @property
    def status_causer(self):
        """The pokemon that caused the status condition"""

        return self.__status_causer

    @status_causer.setter
    def status_causer(self, value):
        if not isinstance(value, PokeMon):
            raise ValueError(f"Invalid status causer {value}")
        self.__status_causer = value

    @property
    def hp(self):
        """The current hp of the pokemon"""
        return self.__hp
    
    @hp.setter
    def hp(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Invalid hp {value}")
        self.__hp = value

    @property
    def name(self):
        """The name of the pokemon"""
        return self.__name

    @name.setter
    def name(self, value):

        if not isinstance(value, str):
            raise ValueError(f"Invalid name {value}")
        self.__name = value

    def fainted(self):
        """Returns True if the pokemon has fainted, else False"""
        return self.__hp == 0


