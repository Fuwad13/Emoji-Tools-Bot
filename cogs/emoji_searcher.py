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
        add_button_ = False
        if ctx.author.guild_permissions.manage_emojis:
            add_button_ = True
        
        
        end_time = time.time()
        formatter = bv.EmojiLinkSource(el)
        menu = bv.MyMenuPages(formatter, delete_message_after=True, add_button_ = add_button_)
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
    

# class MyMenuPages(ui.View, menus.MenuPages):
# 	def __init__(self, source, *, delete_message_after=False):
# 		super().__init__(timeout=120)
# 		self._source = source
# 		self.current_page = 0
# 		self.ctx = None
# 		self.message = None
# 		self.delete_message_after = delete_message_after
		

# 	async def start(self, ctx, *, channel=None, wait=False):
# 		# We wont be using wait/channel, you can implement them yourself. This is to match the MenuPages signature.
# 		await self._source._prepare_once()
# 		self.ctx = ctx
# 		self.message = await self.send_initial_message(ctx, ctx.channel)

# 	async def _get_kwargs_from_page(self, page):
# 		"""This method calls ListPageSource.format_page class"""
# 		value = await super()._get_kwargs_from_page(page)
# 		if 'view' not in value:
# 			value.update({'view': self})
# 		return value

# 	async def interaction_check(self, interaction):
# 		"""Only allow the author that invoke the command to be able to use the interaction"""
# 		return interaction.user == self.ctx.author

# 	async def on_timeout(self):
# 		for i in self.children:
# 			i.disabled = True
# 		await self.message.edit(view = self)

	
	

# 	@ui.button(emoji='<:before_fast_check:754948796139569224>', style=discord.ButtonStyle.blurple)
# 	async def first_page(self, button, interaction):
# 		await self.show_page(0)

# 	@ui.button(emoji='<:before_check:754948796487565332>', style=discord.ButtonStyle.blurple)
# 	async def before_page(self, button, interaction):
# 		await self.show_checked_page(self.current_page - 1)

# 	@ui.button(emoji='<:stop_check:754948796365930517>', style=discord.ButtonStyle.blurple)
# 	async def stop_page(self, button, interaction):
# 		self.stop()
# 		if self.delete_message_after:
# 			await self.message.delete(delay=0)

# 	@ui.button(emoji='<:next_check:754948796361736213>', style=discord.ButtonStyle.blurple)
# 	async def next_page(self, button, interaction):
# 		await self.show_checked_page(self.current_page + 1)

# 	@ui.button(emoji='<:next_fast_check:754948796391227442>', style=discord.ButtonStyle.blurple)
# 	async def last_page(self, button, interaction):
# 		await self.show_page(self._source.get_max_pages() - 1)

# 	@ui.button(emoji = '<:download:316264057659326464>', style = discord.ButtonStyle.green)
# 	async def add_emoji(self, button, intr):
# 		confirm_view = ConfirmOrCancel(self.ctx, timeout = 15)

# 		if not intr.user.guild_permissions.manage_emojis:
# 				await intr.response.send_message("Sorry, you don't have enough permissions to add emojis in this server.", ephemeral = True)
# 		elif intr.user.guild_permissions.manage_emojis:
# 				await intr.response.send_message("**The selected emoji will be added to your server! Are you sure to add this emoji?**`(you have 15 seconds to choose)`", view = confirm_view)
# 				await confirm_view.wait()
# 				if confirm_view.value == True:

# 						await self.ctx.send("Adding the selected emoji!!")
# 						confirm_view.clear_items()
# 						await intr.edit_original_message(view = confirm_view)
						
						

# 				elif confirm_view.value == False:
# 						await self.ctx.send("Cancelling.....", delete_after = 5)
# 						confirm_view.clear_items()
# 						await intr.edit_original_message(view = confirm_view)
						
						

# 				elif confirm_view.value == None:
# 						await self.ctx.send("You took too long to response!! Cancelling...", delete_after = 5)
# 						confirm_view.clear_items()
# 						await intr.edit_original_message(view = confirm_view)
						


			



	


# class EmojiLinkSource(menus.ListPageSource):
# 	def __init__(self, data):
# 		super().__init__(data, per_page=1)
		

	

# 	async def format_page(self, menu, entries):
# 		page = menu.current_page
# 		max_page = self.get_max_pages()
# 		starting_number = page * self.per_page + 1
# 		name = entries.split('#')[0]
# 		url = entries.split('#')[1]
# 		async with aiohttp.ClientSession() as ss:
# 		  async with ss.get(url) as ress:
# 			  r = ress

# 		n_url = r.url
		
# 		embed = discord.Embed(
# 			title=f"Search Results[{page + 1}/{max_page}]",
# 			description=f"{name}",
# 			color=0xffcccb
# 		)
# 		embed.set_image(url = n_url)
# 		author = menu.ctx.author
# 		# author.avatar in 2.0
# 		embed.set_footer(
# 			text=f"Requested by {author}", icon_url=author.avatar.url)
# 		return embed

