import discord
from discord.ext import commands


class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(UtilityCog(bot))
