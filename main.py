from src.pokemon import PokeMon
from src.turn_processor import TinaTurner
from src.player import Player
from typing import List, Dict, Union


def parse_file(txt_file) -> List[str]:
    with open(txt_file) as file:
        return [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("showdown_file", help="The file to process")
    args = parser.parse_args()

    lines = parse_file(args.showdown_file)

    turn, turns, start = [], [], False

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
                turn_processor = TinaTurner(turns, player1=player1, player2=player2)
                player1, player2 = turn_processor.return_players()
            turns = []
        if not start:
            continue

        turns.append(line)

    

    # print(turns[2])
    # print(pp.p1_dict_getter())
