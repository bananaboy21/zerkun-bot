import discord
import sys
import os
import io
from discord.ext import commands
bot = commands.Bot(command_prefix=commands.when_mentioned_or('+'),description="Zerkun Design's Discord bot.\n\nHelp Commands",owner_id=277981712989028353)



@bot.event
async def on_ready():
    print('Bot is online, and ready to ROLL!')
    await bot.change_presence(game=discord.Game(name="Twitter: @ZerkunDesigns"))
    
    
@bot.command()
async def ping(ctx):
    """Premium ping pong giving you a websocket latency."""
    color = discord.Color(value=0x00ff00)
    em = discord.Embed(color=color, title='PoIIIng! Your supersonic latency is:')
    em.description = f"{bot.latency * 1000:.4f} ms"
    await ctx.send(embed=em)
    
    
@bot.command()
async def invite(ctx):
    """Allow my bot to join the hood. YOUR hood."""
    await ctx.send("Invite me to your server: https://discordapp.com/oauth2/authorize?client_id=407676169668788234&scope=bot&permissions=8")
    
    
if not os.environ.get('TOKEN'):
    print("ERROR: Bot token not found.")
bot.run(os.environ.get('TOKEN').strip('"'))
    

