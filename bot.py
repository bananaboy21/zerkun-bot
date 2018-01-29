import discord
import sys
import os
import io
from discord.ext import commands
bot = commands.Bot(command_prefix=commands.when_mentioned_or('*!'),description="Zerkun Design's Discord bot.\n\nHelp Commands",owner_id=277981712989028353)



@bot.event
async def on_ready():
    print('Bot is online, and ready to ROLL!')
    while True:
        await bot.change_presence(game=discord.Game(name=f"with {len(bot.guilds)} servers!"))
