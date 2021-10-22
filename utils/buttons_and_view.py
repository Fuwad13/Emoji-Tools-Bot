import discord
from discord.ui import View, Button
import discord.ui
from discord import ui
from discord.ext import menus
from itertools import starmap, chain
import aiohttp


class HelpPageButton(discord.ui.View):
    def __init__(self, ctx, emb1, emb2):
        super().__init__(timeout=120.0)
        self.page1 = emb1
        self.page2 = emb2
        self.ctx = ctx
        self.add_item(discord.ui.Button(label="Invite", emoji='<:website:877638561501950003>', style=discord.ButtonStyle.green,
                                        url="https://discord.com/oauth2/authorize?client_id=875861419801862165&permissions=138513009728&scope=bot%20applications.commands"))

        self.add_item(discord.ui.Button(label="Vote", emoji='<:discordbotlist:880695425710063646>', style=discord.ButtonStyle.green,
                                        url="https://top.gg/bot/875861419801862165/vote/"))

    async def interaction_check(self, intr):
        if not self.ctx.author == intr.user:
          await intr.response.send_message(f"Only {self.ctx.author.mention} can use these buttons, type `ethelp` to get yours", ephemeral=True)
        return self.ctx.author == intr.user

    # async def on_error(self, error, item, interaction):
    #     await interaction.response.send_message(f"Only {self.ctx.author.mention} can use this button", ephemeral=True)

    @discord.ui.button(emoji='\U000025c0', style=discord.ButtonStyle.blurple)
    async def page_one(self, button: discord.ui.Button, interaction: discord.Interaction):
        button.disabled = True
        self.page_two.disabled = False

        await interaction.message.edit(embed=self.page1, view = self)
        
        
    @discord.ui.button(emoji='\U000025b6', style=discord.ButtonStyle.blurple)
    async def page_two(self, button: discord.ui.Button, interaction: discord.Interaction):

        button.disabled = True
        self.page_one.disabled = False
        await interaction.message.edit(embed=self.page2, view = self)
    
    @discord.ui.button(emoji='\U0001f4f0', style = discord.ButtonStyle.green, label = "Updates")
    async def updates_new(self, button, interaction):
        up_emb = discord.Embed(title="What's new? [v 1.1]", description="`1.` Help command embed looks better now\n`2.` Added cooldown to commands that adds emojis. (to prevent spam and abuse)\n`3.` Exclusive voter command `etsearch` added, you can search for emojis using this command.\n`4.` `etemoji` command now has a delete and a emoji link button\n`5.` Sticker commands are coming soon, stay tuned\n⚠️Warning⚠️\nPlease don't try to add 25 or more emojis in under 10 minutes or fewer, it will result your guild to be ratelimited from adding more emojis! So, be patient and add emojis slowly\n**And please vote for me**", color=0x2F3136)
        await interaction.message.edit(embed = up_emb)

    async def on_timeout(self):
        c = 0
        for item in self.children:
            item.disabled = True
            c+=1
            if c==3:
                break
        await self.message.edit(view = self) 

    
class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, source, *, delete_message_after=False, add_button_ = False):
        super().__init__(timeout=120)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None
        self.delete_message_after = delete_message_after
        self.add_button_ = add_button_

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

    async def on_timeout(self):
        for i in self.children:
            i.disabled = True
        await self.message.edit(view = self)

    
    

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



class DeleteButton(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout= 120)
        self.ctx = ctx

    async def interaction_check(self, intr):
        if not intr.user == self.ctx.author:
            await intr.response.send_message(f"Sorry, only {self.ctx.author.name} can use this button", ephemeral = True)
        
        return self.ctx.author == intr.user
    async def on_timeout(self):
        self.children[0].disabled= True
        await self.message.edit(view = self)

    @ui.button(emoji='<:trashcan:890607299545141358>', style=discord.ButtonStyle.red)
    async def on_deletee(self, button, interaction):
        await self.message.delete()

class SupportServer(discord.ui.View):
    def __init__(self):
        super().__init__(timeout= 180)

        self.add_item(ui.Button(label="Support server",
                            emoji="<:Emoji_tools:883769038600294421>", style=discord.ButtonStyle.url, url="https://discord.gg/zZPf2BUkHm"))
       
