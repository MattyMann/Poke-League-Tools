__Author__ = "Luc Elliott"
__Version__ = "1.0.0"

from .constants import STATUS_CONDITIONS


class PokeMon:
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
        return self.__kills

    @kills.setter
    def kills(self, value):
        self.__kills = value

    @property
    def killed_by(self):
        return self.__killed_by

    @killed_by.setter
    def killed_by(self, value):
        self.__killed_by = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        if status not in STATUS_CONDITIONS:
            raise ValueError(f"Invalid status condition {status}")
        self.__status = status

    @property
    def status_causer(self):
        return self.__status_causer

    @status_causer.setter
    def status_causer(self, value):
        if not isinstance(value, PokeMon):
            raise ValueError(f"Invalid status causer {value}")
        self.__status_causer = value

    @property
    def hp(self):
        return self.__hp
    
    @hp.setter
    def hp(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Invalid hp {value}")
        self.__hp = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Invalid name {value}")
        self.__name = value

    def fainted(self):
        return self.__hp == 0

    def has_fainted(self):
        return True if self.__hp == 0 else False
