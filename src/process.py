import re

import argparse



TERRAIN_MOVES = [
    'Stealth Rock',
    'Spikes',
    'Toxic Spikes',
    'Sticky Web',
]

STATUS_CONDITIONS = [
    'brn',
    'par',
    'psn',
    'tox',
    'slp',
    'frz',
]
 
# battle processer with the name with the intials HP
class HitProcessor(object):
    # class to keep track of different meta data which can be useful
    def __init__(self, name, hp) -> None:
        pass
        

class Playerprocessor(object):
    def __init__(self) -> None:
        self.__p1_dictamon = {}
        self.__p2_dictamon = {}
    

    def __repr__(self) -> str:
        return f"Playerprocessor({self.__p1}, {self.__p2})"

    @property
    def p1(self):
        return self.__p1
    
    @p1.setter
    def p1(self, player):
        self.__p1 = player

    @property
    def p2(self):
        return self.__p2
    
    @p2.setter
    def p2(self, player):
        self.__p2 = player

    @property
    def pokemon(self, p1=False, p2=False):
        if p1:
            return self.__p1_dictamon
        elif p2:
            return self.__p2_dictamon
        else:
            return self.__p1_dictamon, self.__p2_dictamon
        
    
    def add_pokemon(self, poke, p1=False, p2=False):
        if not p1 and not p2:
            raise ValueError("Need to specify which player to set")
        if p1:
            d = self.__p1_dictamon
            
        if p2:
            d = self.__p2_dictamon
    
        d[poke] = {
            'kills': 0,
            'killed_by': None,
            'status': None,
            'status_causer': None,
            'hp': 100,
        }
    
    def update_pokemon(self, poke, key, value, p1=False, p2=False):
        if not p1 and not p2:
            raise ValueError("Need to specify which player to set")
        if p1:
            d = self.__p1_dictamon
            
        if p2:
            d = self.__p2_dictamon

        d[poke][key] = value

    def p1_dict_getter(self):
        # temp functions to call them
        return self.__p1_dictamon

    def p2_dict_getter(self):
        return self.__p2_dictamon


class TinaTurner(object):

    def __init__(self, turns) -> None:
        self.turn_details = {
            'p1poke': None,
            'p2poke': None,
            'p1terrain': None,
            'p2terrain': None,
            'p1hp': None,
            'p2hp': None,
            'p1status_causer': None,
            'p2status_causer': None,
            'p1activate_causer': None,
            'p2activate_causer': None,

        }
        for turn in turns:
            player = self.player(turn)
            
            if turn.startswith('|-damage|') and player:
                self.damage(turn, player)
                
            elif turn.startswith('|move|') and player:
                self.terrain_check(turn, player)
                self.pokemons(turn)
            
            elif turn.startswith('|-status|') and player:
                self.status_setter(player)

            elif turn.startswith('|-activate|') and player:
                self.activate_setter(player)
                # this is for damage from status conditions

            elif turn.startswith('|-heal|') and player:
                print(turn)
                self.damage(turn, player)


    def status_setter(self, player):
        if player == "p1":
            key = 'p1status_causer'
            player = 'p2'
        else:
            key = 'p2status_causer'
            player = 'p1'
        
        self.turn_details[key] = self.turn_details[player + 'poke']

    def activate_setter(self, player):
        if player == "p1":
            key = 'p1activate_causer'
            player = 'p2'
        else:
            key = 'p2activate_causer'
            player = 'p1'
        
        self.turn_details[key] = self.turn_details[player + 'poke']

    
    def damage(self, turn, player):
        # 78\\/100 this is the damage # want to get the first number

        damage = re.compile(r'\d+\\/100')
        fnt = re.compile(r'fnt')
        if damage.search(turn):
            damage = damage.search(turn).group()[:-5]
            if player == "p1":
                self.turn_details['p1hp'] = damage
            else:
                self.turn_details['p2hp'] = damage
        elif fnt.search(turn):
            if player == "p1":
                self.turn_details['p1hp'] = 0
            else:
                self.turn_details['p2hp'] = 0

    
    def terrain_check(self, turn, player):
        if not turn.split('|')[3] in TERRAIN_MOVES:

            return False
        
        if player == "p1":
            self.turn_details['p1terrain'] = turn.split('|')[3]
        else:
            self.turn_details['p2terrain'] = turn.split('|')[3]

    def pokemons(self, turn):
        # re compile this |move|p2a: Dragonite|Fire Spin|p1a: Drifblim to get both Dragonite and Drifblim
        

        pokemon_search = re.compile(r'p[1-2]a: [A-Za-z]+')
        pokemons = pokemon_search.findall(turn)
        if pokemons:
            for pokemon in pokemons:
                if pokemon.startswith('p1'):
                    self.turn_details['p1poke'] = pokemon.split(' ')[-1]
                else:
                    self.turn_details['p2poke'] = pokemon.split(' ')[-1]


        # pokemon = turn.split('|')[2].split(' ')[-1]
        # self.turn_details[key] = pokemon

            

    def player(self, turn):
        player_search = re.compile(r'p[1-2]a')
        turn = "|".join(turn.split('|')[:3])
        if player_search.search(turn):
            return player_search.search(turn).group()[:-1]
        else:
            return None

    
def deliner(txt_file):
        with open(txt_file) as file:
            return [line.strip() for line in file.readlines()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--html')

    args = parser.parse_args()

    lines = deliner(args.html)
    
    turn, turns, start = [], [], False

    pp = Playerprocessor()
    for line in lines:
        if line.startswith("|player|"):
            # gets player information
            if line.split('|')[2] == "p1":
                p1 = line.split('|')[3]
                pp.p1 = p1
            else:
                p2 = line.split('|')[3]
                pp.p2 = p2
            
        
        if line.startswith("|poke|"):  
            poke = line.split('|')[3]
            poke = " ".join(poke.split(' ')[:-1]) \
                if len(poke.split(' ')) > 1 else poke.split(' ')[0] # double check
            # gets pokemon information
            if line.split('|')[2] == "p1":
                
                pp.add_pokemon(poke, p1=True)
            else:
                pp.add_pokemon(poke, p2=True)

        elif line.startswith(("|turn|","|win|")):
            # starts the turn logic
            
            start = True 
            if turns:
                tt = TinaTurner(turns)
                
                print(tt.turn_details)
            turns = []
        if not start:
            continue
        

        turns.append(line)

    # print(turns[2])
    # print(pp.p1_dict_getter())



