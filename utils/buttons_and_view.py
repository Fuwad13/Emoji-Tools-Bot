import discord
from discord.ui import View, Button
import discord.ui
from discord import ui
from discord.ext import menus
from itertools import starmap, chain
import aiohttp

class HelpPageButton(discord.ui.View):
    def __init__(self, ctx, emb1, emb2):
        super().__init__(timeout=60.0)
        self.page1 = emb1
        self.page2 = emb2
        self.ctx = ctx
        self.add_item(discord.ui.Button(label="Invite me", style=discord.ButtonStyle.url,
                                        url="https://discord.com/api/oauth2/authorize?client_id=875861419801862165&permissions=1074121792&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D875861419801862165%26permissions%3D1074064448%26scope%3Dbot&scope=bot%20applications.commands"))

    async def interaction_check(self, intr):
        if not self.ctx.author == intr.user:
          await intr.response.send_message(f"Only {self.ctx.author.mention} can use this button", ephemeral=True)
        return self.ctx.author == intr.user

    # async def on_error(self, error, item, interaction):
    #     await interaction.response.send_message(f"Only {self.ctx.author.mention} can use this button", ephemeral=True)

    @discord.ui.button(label="Page 1", style=discord.ButtonStyle.green)
    async def page_one(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.disabled = True

        await interaction.message.edit(embed=self.page1)
        
        

    @discord.ui.button(label="Page 2", style=discord.ButtonStyle.green)
    async def page_two(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.edit(embed=self.page2)

    
class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, source, *, delete_message_after=False):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None
        self.delete_message_after = delete_message_after

    async def start(self, ctx, *, channel=None, wait=False):
        # We wont be using wait/channel, you can implement them yourself. This is to match the MenuPages signature.
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        """This method calls ListPageSource.format_page class"""
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        """Only allow the author that invoke the command to be able to use the interaction"""
        return interaction.user == self.ctx.author

    @ui.button(emoji='<:before_fast_check:754948796139569224>', style=discord.ButtonStyle.blurple)
    async def first_page(self, button, interaction):
        await self.show_page(0)

    @ui.button(emoji='<:before_check:754948796487565332>', style=discord.ButtonStyle.blurple)
    async def before_page(self, button, interaction):
        await self.show_checked_page(self.current_page - 1)

    @ui.button(emoji='<:stop_check:754948796365930517>', style=discord.ButtonStyle.blurple)
    async def stop_page(self, button, interaction):
        self.stop()
        if self.delete_message_after:
            await self.message.delete(delay=0)

    @ui.button(emoji='<:next_check:754948796361736213>', style=discord.ButtonStyle.blurple)
    async def next_page(self, button, interaction):
        await self.show_checked_page(self.current_page + 1)

    @ui.button(emoji='<:next_fast_check:754948796391227442>', style=discord.ButtonStyle.blurple)
    async def last_page(self, button, interaction):
        await self.show_page(self._source.get_max_pages() - 1)


class EmojiLinkSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)
        

    

    async def format_page(self, menu, entries):
        page = menu.current_page
        max_page = self.get_max_pages()
        starting_number = page * self.per_page + 1
        name = entries.split('#')[0]
        url = entries.split('#')[1]
        async with aiohttp.ClientSession() as ss:
          async with ss.get(url) as ress:
              r = ress

        n_url = r.url
        
        embed = discord.Embed(
            title=f"Search Results[{page + 1}/{max_page}]",
            description=f"{name}",
            color=0xffcccb
        )
        embed.set_image(url = n_url)
        author = menu.ctx.author
        # author.avatar in 2.0
        embed.set_footer(
            text=f"Requested by {author}", icon_url=author.avatar.url)
        return embed
