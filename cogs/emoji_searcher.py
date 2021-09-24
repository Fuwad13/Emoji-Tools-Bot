import discord
import aiohttp
from bs4 import BeautifulSoup
from discord.ext import commands
import asyncio
import time
from utils import buttons_and_view as bv

class EmojiSearcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    async def get_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:

                return await res.text()

    async def get_emojis(self, s_query):
        url = "https://slackmojis.com/emojis/search?utf8=%E2%9C%93&authenticity_token=%2B7uTmZ71dGCT5MsM8Vb8uuVzTxZ7g9ml6YRAPY8gkGHO2TXziuhMvBDCw0geM2IKzTRa%2BWNRC1zJnPIs7boTFg%3D%3D&query=" + \
            str(s_query)
        
        soup_text = await self.get_url(url)
        soup = BeautifulSoup(soup_text, "html.parser")
        e_list = soup.find_all("li")

        final_list = []
        for e in e_list:
            name = e["title"]
            link = "https://slackmojis.com/" + str(e.a["href"])
            s = name + "#" + link
            final_list.append(s)

        return final_list

    @commands.command(name="search", aliases=["find", "srch"], brief="Searches for emojis by the name provided(cooldown = 15 sec)", help="Search for an emoji by name from online. Choose from the search result to add to your server", description="Search for an emoji by name from online. Choose from the search result to add to your server. This command will be available to voters only")
    @commands.guild_only()
    @commands.cooldown(1,15, type = commands.BucketType.user)
    
    async def search(self, ctx, *, name: str):
        start_time = time.time()
        x = name.replace(" ", "+")
        el = await self.get_emojis(x)
        
        end_time = time.time()
        formatter = bv.EmojiLinkSource(el)
        menu = bv.MyMenuPages(formatter, delete_message_after=True)
        await menu.start(ctx)

    @search.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown, retry after `{error.retry_after:.2f}` seconds")
        elif isinstance(error, IndexError):
            await ctx.send("Couldn't find anything , sorry")

        else :
            await ctx.send(f"Something went wrong, can't find anything about that.")
            print(error)
        


def setup(bot):
    bot.add_cog(EmojiSearcher(bot))
    
