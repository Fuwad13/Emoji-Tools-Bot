import discord
from discord.ext import commands
import aiohttp
import typing
from discord import ui
from utils import buttons_and_view as bv


class EmojiManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add", aliases=["create"], brief="Adds/creates an emoji to your server", help="Add a custom emoji from an external server. Name is optional, defaults to the source emoji's name", description="Add emojis from external servers. You need nitro to use this command as you can't use external server emojis without nitro. Make sure you put space between the command name and the emoji.")
    @commands.guild_only()
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.has_permissions(manage_emojis=True)
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
        # await colch.send(f"Added {cm} in server :{ctx.guild.name} with id {ctx.guild.id}\nEmoji name : `{cm.name}`\n{cm.url}")

    @add.error
    async def add_error(self, ctx, error):
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

    @commands.command(name="addurl", aliases=["addlink"], brief="Adds a custom emoji to the server from the provided discord attachment url(image/gif)", help="Add/create a custom emoji from a discord attachment url.Copy the attachment url(must be a discord attachment) and use in the command.", description="Add emoji from an attachment url. The url must be a **discord attachment** url. Using tenor/giphy links won't work")
    @commands.guild_only()
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.has_permissions(manage_emojis=True)
    async def addurl(self, ctx, url: str, name: str = None):
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

    @commands.command(name="addfile", aliases=["addimg", "addf"], brief="Adds/creates a custom emojis from the image file", help="Upload a image file with the command `addfile [name]`as comment to upload it as an emoji in the server. File size can't exceed 256.0 kb", description="Create custom emoji from your device's image files. File size can't exceed 256.0 kb or else the command will not work!")
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

    @commands.command(name="addmany", aliases=["addm", "createmany"], brief="Adds multiple emojis at once! Currently upto 5 emojis at once", help="Add multiple emojis at once in your server. Currently it can add 5 emojis at once to prevent rate-limits of discord!", description="This command can be used to add emojis at a faster rate. It has a cooldown of 10 seconds though (to prevent the bot from being rate-limited)")
    @commands.guild_only()
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.has_permissions(manage_emojis=True)
    @commands.cooldown(1, 10, type=commands.BucketType.guild)
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
    async def addmany_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.NoPrivateMessage):
            await ctx.channel.send("**This command is only executable in server channels!!**")
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.channel.send(f"{ctx.author.mention} You need the `manage emojis` permission to execute this command!")
        elif isinstance(error, discord.ext.commands.BotMissingPermissions):
            await ctx.channel.send(f"{self.bot.user.mention} needs `Manage Emojis` permission to execute this command!")
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.channel.send(f"This command is on cooldown (to prevent the bot from being rate-limited)\n Please retry after {error.retry_after:.2f} seconds")
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.channel.send("**Please put emojis after** `etaddmany`")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.channel.send("**Please put emojis after ** `etaddmany`")
        else:
            await ctx.channel.send(f"`ERROR:` {error}")

    @commands.command(name="delete", aliases=["remove", "del", "rem"], brief="Deletes an emoji from server.", help="Delete a custom emoji using this command", description="Use this command cautiously as this can't be undone.")
    @commands.guild_only()
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.has_permissions(manage_emojis=True)
    async def delete(self, ctx, emoji: discord.Emoji):
        emoname = emoji.name
        await emoji.delete()
        await ctx.channel.send(f"Deleted emoji :`{emoname}`")

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.NoPrivateMessage):
            await ctx.channel.send("**This command is only executable in server channels!!**")
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.channel.send(f"{ctx.author.mention} You need the `manage emojis` permission to execute this command!", delete_after=15)
        elif isinstance(error, discord.ext.commands.BotMissingPermissions):
            await ctx.channel.send(f"{self.bot.user.mention} needs `Manage Emojis` permission to execute this command!")
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.channel.send("**Please put an emoji after** `etdelete` to delete the emoji\nExample: `etdelete <emoji_to_be_deleted> `")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.channel.send("**Please put an emoji after ** `etdeletemany` to delete!")
        else:
            await ctx.send(f"Error: `{error}`")

    @commands.command(name="deletemany", aliases=["delm", "removemany", "removem"], brief="Deletes multiple emojis at once(maximum 5 emojis per command)", help="Deletes multiple emojis at once. You must pass the emojis that are in this guild and put spaces between the emojis.", description="This command can be useful when you want to delete multiple emojis from your server. You can delete upto 5 emojis per command and this command has a cooldown of 10 seconds.**Make sure you put spaces between the emojis**")
    @commands.guild_only()
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.has_permissions(manage_emojis=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
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
            await ctx.channel.send(f"{self.bot.user.mention} needs `Manage Emojis` permission to execute this command!")
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.channel.send(f"This command is on cooldown (to prevent the bot from being rate-limited)\n Please retry after {error.retry_after:.2f} seconds")
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.channel.send("**Please put emojis after** `etdeletemany`")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.channel.send("**Please put emojis after ** `etdeletemany`")

    @commands.command(name="rename", aliases=["ren"], brief="Renames an emoji, use **_** instead of space between words.", help="Renames an emoji to the name you provide , don't use space between the words of new name. Use `_` instead", description="This command is useful to rename any emoji in your server.")
    @commands.guild_only()
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.has_permissions(manage_emojis=True)
    async def rename(self, ctx, emoji: discord.Emoji, new_name):
        emid = emoji.id
        await emoji.edit(name=new_name)
        em = self.bot.get_emoji(emid)
        await ctx.channel.send(f"Renamed  {str(em)} to `{new_name}`")

    @rename.error
    async def rename_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.NoPrivateMessage):
            await ctx.channel.send("**This command is only executable in server channels!!**")
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.channel.send(f"{ctx.author.mention} You need the `manage emojis` permission to execute this command!", delete_after=15)
        elif isinstance(error, discord.ext.commands.BotMissingPermissions):
            await ctx.channel.send(f"{self.bot.user.mention} needs `Manage Emojis` permission to execute this command!")
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.channel.send("**Please put an emoji and the name after **`etrename`** to rename**\nExample: `etrename <emoji> new_name `")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.channel.send("**Please put an emoji and the name after **`etrename`** to rename**\nExample: `etrename <emoji> new_name `")
        else:
            await ctx.send(f"Error: `{error}`")

    @commands.command(name="lock", aliases=["restrict"], brief="Locks an emoji for everyone except the roles mentioned.(admins only command)", help="Locks an emoji for everyone except the roles mentioned. Make sure you mention your role so you can access the emoji and unlock it later. Useful for nsfw emojis to hide.", description="This command can be used to hide/ lock any emojis from everyone except the roles mentioned when locking. Make sure you mention your role too.")
    @commands.guild_only()
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx, emoji: discord.Emoji, roles: commands.Greedy[discord.Role]):
        emo = str(emoji)
        sr = discord.utils.get(ctx.guild.roles, name='Emoji Tools')
        roles.append(sr)

        await emoji.edit(roles=roles)
        rolelist = []
        for i in roles:
            t = f"{i.mention}"
            rolelist.append(t)

        em = discord.Embed(
            title=f"**__Successfully locked__** {emo}", description=f"*Only these roles can access this emoji:*\n\n{rolelist}\n\n\nTo unlock:\ntype: `etunlock` {emo}")
        em.set_footer(icon_url=ctx.author.avatar.url,
                      text=f"Locked by {ctx.author}")
        await ctx.channel.send(embed=em)

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.NoPrivateMessage):
            await ctx.channel.send("**This command is only executable in server channels!!**")
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.channel.send(f"{ctx.author.mention} You need the `administrator` permission to execute this command!!")
        elif isinstance(error, discord.ext.commands.BotMissingPermissions):
            await ctx.channel.send(f"{self.bot.user.mention} needs `Manage Emojis` permission to execute this command!")
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.channel.send("**Error executing command**!!\nCorrect way: `etlock <emoji> <@roles>`")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.channel.send("Missing required arguments! see `ethelp lock` for more")

    @commands.command(name="unlock", aliases=["ul"], brief="Unlocks an emoji for everyone that was locked before.(admins only command)", help="Unlock an emoji that was locked before . You need admin perms . If you don't have access to the emoji then use the emoji name to unlock.", description="This command can be used to unlock an emoji that was locked before. If you can't access the emoji then you may use the emoji name / id in the emoji parameter to unlock.")
    @commands.guild_only()
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx, emoji: discord.Emoji):
        emo = str(emoji)
        await emoji.edit(roles=[ctx.guild.default_role])
        await ctx.channel.send(f"unlocked {emo} for everyone")

    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.NoPrivateMessage):
            await ctx.channel.send("**This command is only executable in server channels!!**")
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.channel.send(f"{ctx.author.mention} You need the `administrator` permission to execute this command!!")
        elif isinstance(error, discord.ext.commands.BotMissingPermissions):
            await ctx.channel.send(f"{self.bot.user.mention} needs `Manage Emojis` permission to execute this command!")
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.channel.send("**Error executing command**!!\nCorrect way: `etunlock <emoji>`")
        elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.channel.send("Missing required arguments! see `ethelp unlock` for more")

    @commands.command(name="emoji", aliases=["moji", "emote", "emojiinfo", "download"], brief="Shows information about the an emoji.", help="Shows information (name, id, creation time, link etc) about the emoji provided. Useful when you want to download any emoji.", description="Get emoji name , id, time of creation etc in an embed.")
    async def emoji(self, ctx, emoji: typing.Union[discord.PartialEmoji, discord.Emoji]):
        url = emoji.url
        name = f"`name:` **{emoji.name}**"
        t = f"`created at:` <t:{int(emoji.created_at.timestamp())}>"
        emid = f"`id:` {emoji.id}"
        text = f"{name}\n{emid}\n{t}"
        emby = discord.Embed(title="Emoji Informations",
                             description=f"{text}\n`animated?:` {str(emoji.animated)}", timestamp=ctx.message.created_at, color=0x2F3136)
        emby.set_author(icon_url=self.bot.user.avatar.url, name="Emoji Tools")
        emby.set_image(url=url)
        emby.set_footer(icon_url=ctx.author.avatar.url,
                        text=f"Requested by {ctx.author}")

        view = bv.DeleteButton()
        view.add_item(ui.Button(label="Emoji Link",
                      style=discord.ButtonStyle.url, url=url))

        msg = await ctx.reply(embed=emby, mention_author=False, view=view)
        view.message = msg

    @emoji.error
    async def emoji_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandError):
            emob = discord.Embed(
                title="`Correct syntax:` etemoji <emoji>  ", color=0x2F3136)
            await ctx.channel.send(content=f"`Emoji not found`", embed=emob)


def setup(bot):
    bot.add_cog(EmojiManager(bot))
