# -*- coding: utf-8 -*-
"""
Created on Fri May  5 22:55:22 2023

@author: matth
"""
import discord
import savereplay
import coachdata
from discord.ext import commands


#initialises the bot and sets permissions
intents = discord.Intents().all()
permissions = discord.Permissions.all()
bot = commands.Bot(command_prefix='/', intents=intents)


currentSeason = 2

#takes a html attachment and stores it in the database
@bot.command()
async def save_replay(ctx, attachment: discord.Attachment):
    await savereplay.Save_replay(ctx, attachment)

                           
# adds a player to the coach database and updates the coach csv
@bot.command()
async def add_player(ctx, name, discord, team, showdown):
    await coachdata.Add_player(ctx, name, discord, team, showdown)    
   

bot.run('MTEwNDE1MjEwNjE0OTEwNTcyNQ.GEhABK.xpNOk3zpRociGPinRR3JGbk59OhP8PIrcZl1SU')




