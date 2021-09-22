import discord
from discord.ext import commands
import aiohttp

class EmojiManager(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(name = "add", aliases= ["create"], brief = "Adds/creates an emoji to your server", help= "Add a custom emoji from an external server. Name is optional, defaults to the source emoji's name", description = "Add emojis from external servers. You need nitro to use this command as you can't use external server emojis without nitro. Make sure you put space between the command name and the emoji.")
	@commands.guild_only()
	@commands.bot_has_permissions(manage_emojis = True)
	@commands.has_permissions(manage_emojis = True)
	async def add(self, ctx, emoji: discord.PartialEmoji, *, name: str = None):

	  url = f"{emoji.url}"
	  if not name:
		  name = emoji.name

	  async with aiohttp.ClientSession() as session:
		  async with session.get(url) as response:
			  img = await response.read()
	  cm = await ctx.guild.create_custom_emoji(name=name, image=img)
	  
	  await ctx.channel.send(f"Successfully created the emoji {cm}")
	  # for main bot
	  #colch = self.bot.get_channel(885013467587825686)
	  #await colch.send(f"Added {cm} in server :{ctx.guild.name} with id {ctx.guild.id}\nEmoji name : `{cm.name}`\n{cm.url}")
	@add.error
	async def add_error(self,ctx, error):
		if isinstance(error, discord.ext.commands.NoPrivateMessage):
			await ctx.channel.send("**This command is only executable in server channels!!**")
		elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
			await ctx.channel.send(f"{ctx.author.mention} You need the `manage emojis` permission to execute this command!")
		elif isinstance(error, discord.ext.commands.errors.BadArgument):
			await ctx.channel.send("Please put an emoji after `etadd` \n(name is optional)")
		elif isinstance(error, discord.ext.commands.BotMissingPermissions):
			await ctx.channel.send(f"{bot.user.mention} needs `Manage Emojis` permission to execute this command!")
		elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
			await ctx.channel.send("**Please put an emoji after **`etadd`\n example: `etadd <emoji> emoji_name`(name is optional)")
		else:
			await ctx.channel.send(f"`ERROR`: {error}")
	
	@commands.command(name = "addurl", aliases = ["addlink"], brief = "Adds a custom emoji to the server from the provided discord attachment url(image/gif)", help = "Add/create a custom emoji from a discord attachment url.Copy the attachment url(must be a discord attachment) and use in the command.", description = "Add emoji from an attachment url. The url must be a **discord attachment** url. Using tenor/giphy links won't work")
	@commands.guild_only()
	@commands.bot_has_permissions(manage_emojis=True)
	@commands.has_permissions(manage_emojis=True)
	async def addurl(self, ctx, url : str, name : str = None):
		aurl = url
		if not name:
			naam = f"et_emoji{random.randint(1,500)}"
		else:
			naam = name
		async with aiohttp.ClientSession() as session:
			async with session.get(aurl) as response:
				img = await response.read()
		cm = await ctx.guild.create_custom_emoji(name=naam, image=img)
		
		await ctx.channel.send(f"Successfully created the emoji {cm}")
		# colch = self.bot.get_channel(885013467587825686)
		# await colch.send(f"Added {cm} in server :{ctx.guild.name} with id {ctx.guild.id}\nEmoji name : `{cm.name}`\n{cm.url}")
	
	@addurl.error
	async def addurl_error(self, ctx, error):
		if isinstance(error, discord.ext.commands.NoPrivateMessage):
			await ctx.channel.send("**This command is only executable in server channels!!**")

		elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
			await ctx.channel.send(f"{ctx.author.mention} You need `manage_emojis` permission to use this command!")
		elif isinstance(error, discord.ext.commands.BotMissingPermissions):
			await ctx.channel.send("Please make sure I have the `Manage Emojis` permission!")

		else:
			await ctx.channel.send(f"`ERROR`: {error}")
	
	@commands.command(name = "addfile", aliases = ["addimg", "addf"], brief = "Adds/creates a custom emojis from the image file", help = "Upload a image file with the command `addfile [name]`as comment to upload it as an emoji in the server. File size can't exceed 256.0 kb", description = "Create custom emoji from your device's image files. File size can't exceed 256.0 kb or else the command will not work!")
	@commands.guild_only()
	@commands.bot_has_permissions(manage_emojis=True)
	@commands.has_permissions(manage_emojis=True)
	async def addfile(self, ctx, name: str = None):
		try:
			async with ctx.channel.typing():
				attach = str(ctx.message.attachments[0])
				if not name:
					name = f"et_emoji{random.randint(1,500)}"
				async with aiohttp.ClientSession() as session:
					async with session.get(attach) as response:
						img = await response.read()
				cm = await ctx.guild.create_custom_emoji(name=name, image=img)
				await ctx.channel.send(f"Successfully created the emoji {cm}")
				# colch = self.bot.get_channel(885013467587825686)
				# await colch.send(f"Added {cm} in server :{ctx.guild.name} with id {ctx.guild.id}\nEmoji name : `{cm.name}`\n{cm.url}")
		except IndexError:
			await ctx.channel.send("Please provide a valid image or gif file")
		except Exception as e:
			await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')

	@addfile.error
	async def addfile_error(self, ctx, error):
		if isinstance(error, discord.ext.commands.NoPrivateMessage):
			await ctx.channel.send("**This command is only executable in server channels!!**")

		elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
			await ctx.channel.send(f"{ctx.author.mention} You need `manage_emojis` permission to use this command!")
		elif isinstance(error, discord.ext.commands.BotMissingPermissions):
			await ctx.channel.send("Please make sure I have the `Manage Emojis` permission!")
		elif isinstance(error, discord.ext.commands.CommandError):
			await ctx.channel.send(f"`ERROR` : {error}")

	@commands.command(name = "addmany", aliases = ["addm", "createmany"], brief = "Adds multiple emojis at once! Currently upto 5 emojis at once", help = "Add multiple emojis at once in your server. Currently it can add 5 emojis at once to prevent rate-limits of discord!", description = "This command can be used to add emojis at a faster rate. It has a cooldown of 10 seconds though (to prevent the bot from being rate-limited)")
	@commands.guild_only()
	@commands.bot_has_permissions(manage_emojis=True)
	@commands.has_permissions(manage_emojis=True)
	@commands.cooldown(1,10, type = commands.BucketType.guild)
	async def addmany(self, ctx, emojis: commands.Greedy[discord.PartialEmoji]):
		async with ctx.channel.typing():
			emojilist = []
			c = 0
			for x in emojis:
				url = f"{x.url}"

				naam = x.name

				async with aiohttp.ClientSession() as session:
					async with session.get(url) as response:
						img = await response.read()
				cm = await ctx.guild.create_custom_emoji(name=naam, image=img)
				x = str(cm)
				emojilist.append(x)
				await asyncio.sleep(1)
				c += 1
				if c == 5:
					break
			if len(emojilist) != 0:
				await ctx.channel.send(f"Successfully created these emojis {emojilist}")
				# colch = self.bot.get_channel(885013467587825686)
				# await colch.send(f"Added these  {emojilist} in server :{ctx.guild.name} with id {ctx.guild.id}")
			elif len(emojilist) == 0:
				await ctx.channel.send(f"Hey, maybe you forgot to put spaces between the emojis!Try again!!")


	@addmany.error
	async def addmany_error(self,ctx, error):
		if isinstance(error, discord.ext.commands.NoPrivateMessage):
			await ctx.channel.send("**This command is only executable in server channels!!**")
		elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
			await ctx.channel.send(f"{ctx.author.mention} You need the `manage emojis` permission to execute this command!")
		elif isinstance(error, discord.ext.commands.BotMissingPermissions):
			await ctx.channel.send(f"{bot.user.mention} needs `Manage Emojis` permission to execute this command!")
		elif isinstance(error, discord.ext.commands.CommandOnCooldown):
			await ctx.channel.send(f"This command is on cooldown (to prevent the bot from being rate-limited)\n Please retry after {error.retry_after:.2f} seconds")
		elif isinstance(error, discord.ext.commands.errors.BadArgument):
			await ctx.channel.send("**Please put emojis after** `etaddmany`")
		elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
			await ctx.channel.send("**Please put emojis after ** `etaddmany`")
		else:
			await ctx.channel.send(f"`ERROR:` {error}")

	@commands.command(name = "deletemany", aliases = ["delm", "removemany","removem"], brief = "Deletes multiple emojis at once(maximum 5 emojis per command)", help = "Deletes multiple emojis at once. You must pass the emojis that are in this guild and put spaces between the emojis.", description = "This command can be useful when you want to delete multiple emojis from your server. You can delete upto 5 emojis per command and this command has a cooldown of 10 seconds.**Make sure you put spaces between the emojis**")
	@commands.guild_only()
	@commands.bot_has_permissions(manage_emojis=True)
	@commands.has_permissions(manage_emojis=True)
	@commands.cooldown(1,10, commands.BucketType.guild)
	async def deletemany(self, ctx, emojis: commands.Greedy[discord.Emoji]):
		async with ctx.channel.typing():
			c = 0
			demojilist = []
			for x in emojis:
				name = f":{x.name}:"
				await x.delete()
				demojilist.append(name)
				await asyncio.sleep(1)
				c += 1
				if c == 5:
					break
			if len(demojilist) != 0:
				await ctx.channel.send(f"Deleted these emojis: {demojilist}")
			elif len(demojilist) == 0:
				await ctx.channel.send("Hey , did you forget to put spaces between the emojis? Try again!")


	@deletemany.error
	async def deletemany_error(self, ctx, error):
		if isinstance(error, discord.ext.commands.NoPrivateMessage):
			await ctx.channel.send("**This command is only executable in server channels!!**")
		elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
			await ctx.channel.send(f"{ctx.author.mention} You need the `manage emojis` permission to execute this command!", delete_after=15)
		elif isinstance(error, discord.ext.commands.BotMissingPermissions):
			await ctx.channel.send(f"{bot.user.mention} needs `Manage Emojis` permission to execute this command!")
		elif isinstance(error, discord.ext.commands.CommandOnCooldown):
			await ctx.channel.send(f"This command is on cooldown (to prevent the bot from being rate-limited)\n Please retry after {error.retry_after:.2f} seconds")
		elif isinstance(error, discord.ext.commands.errors.BadArgument):
			await ctx.channel.send("**Please put emojis after** `etdeletemany`")
		elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
			await ctx.channel.send("**Please put emojis after ** `etdeletemany`")


def setup(bot):
  bot.add_cog(EmojiManager(bot))
