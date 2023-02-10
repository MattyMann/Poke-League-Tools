# import argparse
# import pandas as pd
import math

# parser = argparse.ArgumentParser()

# parser.add_argument('user_one',help="the first player",type=str)
# parser.add_argument('user_two',help="the second player",type=str)
# parser.add_argument('user_one_fin_mon',help="the pokemon remaining for the first player",type=int,choices=range(7))
# parser.add_argument('user_two_fin_mon',help="the pokemon remaining for the second player",type=int,choices=range(7))
# parser.add_argument('winner',help="which of player one or two won: leave blank for draw",type=str,default="")

# args = parser.parse_args()

##########################

# kval = 32

##########################

def elo_calc(elo: int,vs_elo: int,wld,K) -> int:
    expected = 1/(1 + math.pow(10,(vs_elo-elo)/400))

    new_elo = int(elo + K * (wld - expected))

    return new_elo

##########################

# # Read in the usernames and elos
# ratings = pd.read_csv("ratings",header=None,names=["username","elo"],dtype={'elo': 'int16'},index_col="username")

# user_one_elo = ratings.loc[args.user_one]['elo']

# user_two_elo = ratings.loc[args.user_two]['elo']

# if args.winner == "":
#     # draw case
#     ratings.loc[args.user_one,'elo'] = int(elo_calc(user_one_elo,user_two_elo,0.5,kval))
#     ratings.loc[args.user_two,'elo']= int(elo_calc(user_two_elo,user_one_elo,0.5,kval))
# elif args.winner == args.user_one:
#     ratings.loc[args.user_one,'elo'] = int(elo_calc(user_one_elo,user_two_elo,1,kval*(1 + ((args.user_one_fin_mon - args.user_two_fin_mon)/6))))
#     ratings.loc[args.user_two,'elo'] = int(elo_calc(user_two_elo,user_one_elo,0,kval*(1 + ((args.user_one_fin_mon - args.user_two_fin_mon)/6))))
# elif args.winner == args.user_two:
#     ratings.loc[args.user_one,'elo'] = int(elo_calc(user_one_elo,user_two_elo,0,kval*(1 + ((args.user_two_fin_mon - args.user_one_fin_mon)/6))))
#     ratings.loc[args.user_two,'elo'] = int(elo_calc(user_two_elo,user_one_elo,1,kval*(1 + ((args.user_two_fin_mon - args.user_one_fin_mon)/6))))
# else:
#     raise Exception("Winner is not a player")
