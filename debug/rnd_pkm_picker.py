"""
@created 04/11/2023 - 16:08

@author chris
"""
import random


def get_random_ints():
    rnd_int = None
    picked_ints = list()
    while len(picked_ints) < 6:
        rnd_int = random.randint(0, 10)
        if rnd_int not in picked_ints:
            picked_ints.append(rnd_int)
    return picked_ints


def get_20_rnd_ints():
    rnd_int = None
    picked_ints = ''
    while len(picked_ints) < 20:
        rnd_int = random.randint(0, 9)
        picked_ints += str(rnd_int)
    return picked_ints
