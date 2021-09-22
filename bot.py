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
from utils import buttons_and_view as bv

load_dotenv()  # take environment variables from .env.

# --------tokens and keys-----------------

TOKEN = os.getenv("TOKEN")

# ------------ constants---------------------
COLL_CHANNEL = 885013467587825686
UPTIME_DICT = {"uts": ""}
# ------------extensions --------------------------
intital_extensions = [
    "cogs.emojis",
    "jishaku",
    "cogs.public_commands",
    "cogs.info",
    "cogs.emoji_searcher",
    "cogs.utility"
]

ALL_EXTENSIONS = [
    "cogs.emojis",
	"jishaku",
    "cogs.public_commands",
    "cogs.info",
    "cogs.emoji_searcher",
    "cogs.utility"
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

bot = commands.AutoShardedBot(command_prefix=get_prefix, intents=intents)


if __name__ == "__main__":
    for e in intital_extensions:
        bot.load_extension(e)

# ==== events ==========


@bot.event
async def on_ready():
    UPTIME_DICT["uts"] = str(int(time.time()))
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"ethelp  |  @Emoji Tools help"))
    print(f'logged in as {bot.user}')
    bot.get_command("jishaku").hidden = True


@bot.event
async def on_guild_join(guild):
    idd = guild.id
    name = guild.name
    ec = len(guild.emojis)
    mc = guild.member_count
    em = discord.Embed(
        title=f"Joined {name} ({idd})", description=f"emoji count: {ec}\nmember count: {mc}", color=0xFF0000)
    em.set_footer(text=":", icon_url=guild.icon_url)
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
            title=f"Cogs Loader", description=f"{tick} Successfully Loaded the cog `{cogname}`", timestamp=ctx.message.created_at)
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
            title=f"Cogs Unloader", description=f"{tick} Successfully unloaded the cog `{cogname}`", timestamp=ctx.message.created_at)
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
        title="Success!", description=f"These cogs were loaded successfully!\n{success_s}")
    await ctx.channel.send(embed=em)


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


# ----------Help Command ------------------

class MyHelpCommand(commands.MinimalHelpCommand):
    def __init__(self):

        super().__init__(
            command_attrs={
                'cooldown': commands.CooldownMapping.from_cooldown(1, 3.0, commands.BucketType.member),
                'help': 'Shows help about the bot, a command, or a category',
                'aliases': ["commands", "helo", "hel"],
            }, verify_checks=False, show_hidden=False
        )

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            # Ignore missing permission errors
            if isinstance(error.original, discord.HTTPException) and error.original.code == 50013:
                return

            await ctx.send(str(error.original))

    def get_command_signature(self, command):
        return f"**{self.context.clean_prefix}{command.qualified_name} {command.signature}**\n`{command.brief}`"

    async def send_bot_help(self, mapping):
        embed1 = discord.Embed(title="Help", color=0x90EE90)
        embed2 = discord.Embed(title="Help", color=0x90EE90)
        if self.context.author.id == 428812756456570882:
            self.show_hidden = True
		

        for cog, commands in mapping.items():

            filtered = await self.filter_commands(commands)
            command_signatures = [
                self.get_command_signature(c) for c in filtered]

            for cmd in command_signatures:
                embed1.add_field(
                    name=f"{cmd.split(f'{self.context.clean_prefix}')[1].split(' ')[0]}", value=f"{cmd}")

        channel = self.get_destination()
        view = bv.HelpPageButton(self.context, embed1, embed2)

        msg = await channel.send(embed=embed1,view = view)
        
        

        


bot.help_command = MyHelpCommand()




bot.run(TOKEN)
