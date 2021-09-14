import discord
import aiohttp
from bs4 import BeautifulSoup
from discord.ext import commands, menus
import asyncio
import time


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

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    @commands.bot_has_permissions(manage_emojis=True)
    async def search(self, ctx, *, name: str):
        start_time = time.time()
        x = name.replace(" ", "+")
        el = await self.get_emojis(x)
        em_sr = discord.Embed(title="Search Results......")
        end_time = time.time()
        msg = await ctx.send(f"{end_time - start_time}", embed=em_sr)
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
        current = 0
        for button in buttons:
            await msg.add_reaction(button)
        em_enam = el[current].split('#')[0]
        ur = el[current].split('#')[1]
        embe = discord.Embed(
            title=f"{em_enam}", description=f"[link]({ur})", color=0x90FF90, timestamp=msg.created_at)
        embe.set_image(url=ur)
        await msg.edit(embed=embe)
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons and reaction.message == msg, timeout=60.0)
            except asyncio.TimeoutError:
                for button in buttons:
                    await msg.remove_reaction(button, self.bot.user)
            else:
                previous_page = current
                if reaction.emoji == u"\u23EA":
                    current = 0

                elif reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1

                elif reaction.emoji == u"\u27A1":
                    if current < len(el)-1:
                        current += 1

                elif reaction.emoji == u"\u23E9":
                    current = len(el)-1

                if current != previous_page:
                    em_ename = el[current].split('#')[0]
                    url = el[current].split('#')[1]
                    async with aiohttp.ClientSession() as ss:
                        async with ss.get(url) as ress:
                            r = ress
                    n_url = r.url
                    embed = discord.Embed(
                        title=f"{em_ename}", description=f"[link]({url})", color=0x90FF90, timestamp=msg.created_at)
                    embed.set_image(url=n_url)
                    await msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(EmojiSearcher(bot))
