from math import pow

def elo_calc(elo: int,vs_elo: int,wld,K) -> int:

    expected = 1/(1 + pow(10,(vs_elo-elo)/400))

    new_elo = int(elo + K * (wld - expected))

    return new_elo
