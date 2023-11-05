__Author__ = "Luc Elliott"
__Version__ = "1.0.0"

import re


TERRAIN_MOVES = [
    "Stealth Rock",
    "Spikes",
    "Toxic Spikes",
    "Sticky Web",
    # Add more Terrain moves here
]

STATUS_CONDITIONS = [
    "brn",  # Burn
    "par",  # Paralysis
    "psn",  # Poison
    "tox",  # Toxic
    "slp",  # Sleep
    "frz",  # Freeze
]

# Regex patterns

FAINT = re.compile(r"fnt")
DAMAGE = re.compile(r"\d+\\/100")
POKEMON_SEARCH = re.compile(r"p[1-2]a: [A-Za-z0-9]+")
PLAYER_SEARCH = re.compile(r"p[1-2]a")
