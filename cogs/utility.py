import discord
from discord.ext import commands
from utils import buttons_and_view as bv


class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "@delete", aliases = ["@d"], hidden = True)
    @commands.is_owner()
    async def _devdelete(self, ctx):
        message = ctx.message.reference.resolved
        await message.delete(delay = 1)
    @_devdelete.error
    async def _devdelerror(self, ctx, error):
        await ctx.send(f"No, {error}")

    @commands.command(name = "@send", aliases =["@sendmessage", "@s"], hidden = True)
    @commands.is_owner()
    async def _devsend(self, ctx,server: discord.Guild,*,message: str):
        for ch in server.text_channels:
            try:
                await ch.send(message)
                break
            except:
                pass
        
    @_devsend.error
    async def devsenderror(self, ctx, error):
        await ctx.send(f"{error}")


def setup(bot):
    bot.add_cog(UtilityCog(bot))
