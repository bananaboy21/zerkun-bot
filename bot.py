import discord
import os
import io
import traceback
import sys
import time
import datetime
import asyncio
import random
import aiohttp
import pip
import random
import textwrap
from contextlib import redirect_stdout
from discord.ext import commands
import json
from discord.ext import commands
bot = commands.Bot(command_prefix=commands.when_mentioned_or('='),description="Zerkun Design's Discord bot.\n\nHelp Commands",owner_id=277981712989028353)


def cleanup_code(content):
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')


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
    

@bot.command()
async def twitter(ctx):
    """My Twitter profile."""
    await ctx.send("https://twitter.com/ZerkunDesigns")
    
    
@bot.command()
@commands.has_permissions(manage_messages = True)
async def purge(ctx, num: int):
    """Deletes a # of msgs. *purge [# of msgs].""" 
    try: 
        if num is None:
            await ctx.send("How many messages would you like me to delete? Usage: *purge [number of msgs]")
        else:
            try:
                float(num)
            except ValueError:
                return await ctx.send("The number is invalid. Make sure it is valid! Usage: *purge [number of msgs]")
            await ctx.channel.purge(limit=num+1)
            await ctx.send("Purged successfully :white_check_mark:")
    except discord.Forbidden:
        await ctx.send("Purge unsuccessful. The bot does not have Manage Msgs permission.")
        
        
@bot.command()
@commands.has_permissions(ban_members=True)
async def mute(ctx, user: discord.Member, time=None):
    '''Forces someone to shut up. Usage: *mute [user] [time in mins]'''
    try:
        if time is None:
            await ctx.channel.set_permissions(user, send_messages=False)
            await ctx.send(f"{user.mention} is now forced to shut up. :zipper_mouth: ")
        else:
            try:
                time = time * 60
                float(time)
            except ValueError:
                return await ctx.send("Your time is an invalid number. Make sure...it is a number.")
            await ctx.channel.set_permissions(user, send_messages=False)
            await ctx.channel.send(f"{user.mention} is now forced to shut up. :zipper_mouth: ")
            await asyncio.sleep(time)
            await ctx.channel.set_permissions(user, send_messages=True)
            await ctx.channel.send(f"{user.mention} is now un-shutted up.")
    except discord.Forbidden:
        return await ctx.send("I could not mute the user. Make sure I have the manage channels permission.")
    
    
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user: discord.Member):
    """Kicks a member into the world outside your server."""
    await ctx.send(f"{user.name} has been kicked.")
    await user.kick()
    
    
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user: discord.Member):
    """Bans a member."""
    await ctx.send(f"{user.name} has been banned.")
    await user.ban()
    
    
@bot.command(hidden=True, name='eval')
async def _eval(ctx, *, body: str):

    if not dev_check(ctx.author.id):
        return await ctx.send("HALT! This command is for the devs only. Sorry. :x:")

    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
    }

    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            await ctx.send(f'```py\n{value}{ret}\n```')   
    
    
if not os.environ.get('TOKEN'):
    print("ERROR: Bot token not found.")
bot.run(os.environ.get('TOKEN').strip('"'))
    

