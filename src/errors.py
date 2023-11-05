__Author__ = "Luc Elliott"
__Version__ = "1.0.0"


class PokemonError(Exception):
    # class which handles pokemon errors
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class PlayerError(Exception):
    # class which handles player errors
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
