# --------imports-----------------
from logging import info
import time
import aiohttp
import discord
import random
import asyncio
import typing
import os
from discord.ext import commands, tasks
from discord.ext.commands import BucketType
from dotenv import load_dotenv
from utils import help

load_dotenv()  # take environment variables from .env.

# --------tokens and keys-----------------

TOKEN = os.getenv("TOKEN")

# ------------ constants---------------------
COLL_CHANNEL = 885013467587825686
UPTIME_DICT = {"uts": ""}
# ------------extensions --------------------------
#emoji searcher unstable
intital_extensions = [
    "cogs.emojis",
    "cogs.public_commands",
    "cogs.error_handler",
    "cogs.utility",
    "jishaku"
]

ALL_EXTENSIONS = [
    "cogs.emojis",
    "cogs.emoji_searcher",
    "cogs.public_commands",
    "cogs.error_handler",
    "cogs.utility",
    "jishaku"
]

# -----prefixes------


def get_prefix(bot, message):

    prefixes = [">"]

    if not message.guild:
        # Only allow ? to be used in DMs
        return '>'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

# --------Bot constructor------------------


intents = discord.Intents(messages=True, guilds=True,
                          reactions=True)

bot = commands.AutoShardedBot(command_prefix=get_prefix, intents=intents, case_insensitive = True)


if __name__ == "__main__":
    for e in intital_extensions:
        bot.load_extension(e)

# ==== events ==========


@bot.event
async def on_ready():
    UPTIME_DICT["uts"] = str(int(time.time()))
    bot.uptime = int(UPTIME_DICT["uts"])
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"ethelp  |  {len(bot.users)} users"))
    print(f'logged in as {bot.user}')
    bot.get_command("jishaku").hidden = True


@bot.event
async def on_guild_join(guild):
    idd = guild.id
    name = guild.name
    ec = len(guild.emojis)
    mc = guild.member_count
    em = discord.Embed(
        title=f"Joined {name} ({idd})", description=f"emoji count: {ec}\nmember count: {mc}", color=0x2F3136)
    try:
        em.set_footer(text=f"{name}", icon_url=guild.icon)
    except:
        pass
    channel = bot.get_channel(878420596168462386)
    await channel.send(embed=em)
    channels = await guild.fetch_channels()

    for c in channels:
        try:
            await c.send("**Thanks you for inviting me!!**\n**My prefix is ** `et` or `@Emoji Tools `\ntype `ethelp` to get a list of commands!!\nMake sure i have `send message`, `embed links` and `add reaction` permission in the channel you want to use the commands!")
            break
        except:
            pass


@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(878420596168462386)
    name = guild.name
    await channel.send(f"Left {name} : {guild.id}")
# tasks ----->>>


# dev essential commands
@bot.command(name="loadcog", aliases=['lc', 'loadc'], hidden=True, brief="Loads a cog")
@commands.is_owner()
async def _loadcog(ctx, cogname: str):
    try:
        tick = bot.get_emoji(880695423516430336)
        cname = f"{cogname}"

        bot.load_extension(cname)
        em = discord.Embed(
            title=f"Cogs Loader", description=f"{tick} Successfully Loaded the cog `{cogname}`", timestamp=ctx.message.created_at, color=0x2F3136)
        await ctx.channel.send(embed=em)
    except Exception as e:
        await ctx.channel.send(e)


@_loadcog.error
async def _loadcogerror(ctx, error):
    await ctx.channel.send(f"`Error`: `{error}`")


@bot.command(name="unloadcog", aliases=["uc"], hidden=True, brief="Unloads a cog")
@commands.is_owner()
async def _unloadcog(ctx, cogname: str):

    try:
        tick = bot.get_emoji(880695423516430336)
        cname = f"{cogname}"

        bot.unload_extension(cname)
        em = discord.Embed(
            title=f"Cogs Unloader", description=f"{tick} Successfully unloaded the cog `{cogname}`", timestamp=ctx.message.created_at, color=0x2F3136)
        await ctx.channel.send(embed=em)
    except Exception as e:
        await ctx.channel.send(e)


@_unloadcog.error
async def _unloadcogerror(ctx, error):
    await ctx.channel.send(f"`Error`: `{error}`")


@bot.command(name="reloadall", aliases=["ra", "rela"], hidden=True, brief="Reloads all cogs, [if not loaded previously, then loads the cog]")
@commands.is_owner()
async def reloadall(ctx):
    success_s = ""
    tick = bot.get_emoji(880695423516430336)
    for e in ALL_EXTENSIONS:
        try:
            bot.reload_extension(e)
            tt = f"{str(tick)} `{e.split('cogs.')[-1]}`\n"
            success_s += tt
        except commands.ExtensionNotLoaded:
            bot.load_extension(e)
            tt = f"{str(tick)} `{e.split('cogs.')[-1]}`\n"
            success_s += tt
    em = discord.Embed(
        title="Success!", description=f"These cogs were loaded successfully!\n{success_s}", color=0x2F3136)
    await ctx.channel.send(embed=em)
    bot.get_command("jishaku").hidden = True



@reloadall.error
async def reloadallerror(ctx, error):
    await ctx.channel.send(f"`ERROR` : `{error}`")


@bot.command(name="reloadcog", aliases=["rc", "r"], hidden=True, brief="Reloads a cog")
@commands.is_owner()
async def _reloadcog(ctx, cogname: str):
    try:
        tick = bot.get_emoji(880695423516430336)
        cname = f"{cogname}"
        bot.reload_extension(cname)
        em = discord.Embed(
            title=f"Cogs Reloader", description=f"{tick} Successfully reloaded the cog `{cogname}`", timestamp=ctx.message.created_at)
        await ctx.channel.send(embed=em)
    except commands.ExtensionNotLoaded:
        await ctx.channel.send("This cog was not loaded")


@_reloadcog.error
async def reloaderror(ctx, error):
    await ctx.channel.send(f"`ERROR` : `{error}`")


@bot.command(name = "hidecmd", hidden = True)
@commands.is_owner()
async def _hidecmd(ctx):
    bot.get_command("jishaku").hidden = True
    await ctx.send("Done.. shhhh")


# ----------Help Command ------------------

bot.help_command = help.MyHelpCommand()




bot.run(TOKEN)
