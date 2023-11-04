# -*- coding: utf-8 -*-
"""
Created on Fri May  5 22:55:22 2023

@author: matth & chris
"""
import os
import typing

import discord
from dotenv import load_dotenv

import savereplay
import coachdata
from discord.ext import commands

dotenv_path = 'hidden.env'
load_dotenv(dotenv_path)
bot_token = os.environ.get('TOKEN')
# initialises the bot and sets permissions
intents = discord.Intents().all()
permissions = discord.Permissions.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents)
currentSeason = 2


@bot.event
async def on_ready():
    print("Ready!")


# takes a html attachment and stores it in the database
@bot.slash_command(name='save_replay', description='Saves replay and updates spreadsheet',
                   guild=discord.Object(id=1104155758632902656))
async def save_replay(ctx, attachment: typing.Optional[discord.Attachment]):
    if attachment is None:
        print('You didnt upload anything')
    else:
        await savereplay.Save_replay(ctx, attachment)


# adds a player to the coach database and updates the coach csv
@bot.command()
async def add_player(ctx, name, discord, team, showdown):
    await coachdata.Add_player(ctx, name, discord, team, showdown)


def run_discord_bot():
    bot.run(bot_token)
