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
