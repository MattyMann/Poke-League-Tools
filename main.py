from src.pokemon import PokeMon
from src.turn_processor import TinaTurner
from src.player import Player
from typing import List, Tuple


def parse_file(txt_file) -> List[str]:
    with open(txt_file) as file:
        return [line.strip() for line in file.readlines()]
    

def main(lines: list) -> Tuple[Player, Player]:
    """Main function to process a Pokemon battle
    
    Args:
        lines (list): A list of lines from a Pokemon battle
        
    Returns:
        Tuple[Player, Player]: A tuple of the players in the battle"""
    turns, start = [], False
    for line in lines:
        if line.startswith("|player|"):
            # gets player information
            if line.split("|")[2] == "p1":
                p1_id = line.split("|")[3]
                player1 = Player(p1_id)
            else:
                p2_id = line.split("|")[3]
                player2 = Player(p2_id)

        if line.startswith("|poke|"):
            poke = line.split("|")[3]
            poke = (
                " ".join(poke.split(" ")[:-1])
                if len(poke.split(" ")) > 1
                else poke.split(" ")[0]
            ) 

            poke = poke[:-1] if poke.endswith(",") else poke
            poke = poke.split("-")[0] if "-" in poke else poke
            poke = PokeMon(poke)
            if line.split("|")[2] == "p1":
                player1.add_pokemon(poke)
            else:
                player2.add_pokemon(poke)

        elif line.startswith(("|turn|", "|win|")):
            # starts the turn logic

            start = True
            if turns:
                turn_processor = TinaTurner(
                    turns, player1=player1, player2=player2
                    )
                player1, player2 = turn_processor.return_players()
            turns = []
        if not start:
            continue

        turns.append(line)

    return player1, player2


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("showdown_file", help="The file to process")
    args = parser.parse_args()

    lines = parse_file(args.showdown_file)

    player1, player2 = main(lines)

    print("Player 1 Pokemon")
    print(player1.pokemon)
    print()
    print("Player 2 Pokemon")
    print(player2.pokemon)
    print()
    print("Player 1 Terrain")
    print(player1.terrain)
    print()
    print("Player 2 Terrain")
    print(player2.terrain)
    print()
    print("Player 1")
    print(player1)
    print()
    print("Player 2")
    print(player2)
    print()

