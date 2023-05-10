def elo_calc(elo: int,vs_elo: int, wld: float, K) -> int:
    """
    Calculates new elos based on match results, other elos, and K values.
    --------
    Input
    -----
    elo: the elo to recalculate
    vs_elo: the versus elo
    wld: a number to pass for win, loss, or draw (1,0,0.5) respectively
    K: K value
    
    Output
    -----
    new_elo: the recalculated elo
    """
    expected = 1/(1 + pow(10,(vs_elo-elo)/400))

    new_elo = int(elo + K * (wld - expected))

    return new_elo
