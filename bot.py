#--------imports-----------------
from logging import info
import time, aiohttp, discord, random, asyncio, typing,os
from discord.ext import commands, tasks
from itertools import cycle
from discord.ext.commands import BucketType
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# --------tokens and keys-----------------

TOKEN = os.getenv("TOKEN")

#------------ constants---------------------
COLL_CHANNEL = 885013467587825686
UPTIME_DICT = {"uts": ""}
#------------extensions --------------------------
intital_extensions = [
    "cogs.emojis"
]

ALL_EXTENSIONS = [
    "cogs.emojis",
    "cogs.public_commands",
    "cogs.info",
    "cogs.emoji_searcher",
    "cogs.utility"
]

#-----prefixes------

#will experiment about this later
# def get_prefix(bot, message):

    
#     prefixes = ['>', 'em', 'f']

    
#     if not message.guild:
#         # Only allow ? to be used in DMs
#         return '>'

#     # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
#     return commands.when_mentioned_or(*prefixes)(bot, message)

#--------Bot constructor------------------

intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True, presences=True)

bot = commands.Bot(command_prefix=">", intents=intents)


if __name__ == "__main__":
  for e in intital_extensions:
    bot.load_extension(e)

# dev essential commands 


@bot.command(aliases=['lc'])
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


@bot.command(aliases=["uc"])
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

@bot.command(aliases = ["ra", "rela"])
@commands.is_owner()
async def reloadall(ctx):
  success_s = ""
  tick = bot.get_emoji(880695423516430336)
  for e in ALL_EXTENSIONS:
    try:
      bot.reload_extension(e)
      tt = f"{str(tick)} `{e.split('.')[1]}`\n"
      success_s +=tt
    except commands.ExtensionNotLoaded:
      bot.load_extension(e)
      tt = f"{str(tick)} `{e.split('.')[1]}`\n"
      success_s += tt
  em = discord.Embed(title = "Success!", description = f"These cogs were loaded successfully!\n{success_s}")
  await ctx.channel.send(embed = em)

@reloadall.error
async def reloadallerror(ctx, error):
  await ctx.channel.send(f"`ERROR` : `{error}`")

@bot.command(aliases = ["rc", "r"])
@commands.is_owner()
async def rreloadcog(ctx, cogname: str):
  try:
    tick = bot.get_emoji(880695423516430336)
    cname = f"{cogname}"
    bot.reload_extension(cname)
    em = discord.Embed(
        title=f"Cogs Reloader", description=f"{tick} Successfully reloaded the cog `{cogname}`", timestamp=ctx.message.created_at)
    await ctx.channel.send(embed=em)
  except commands.ExtensionNotLoaded:
      await ctx.channel.send("This cog was not loaded")


@rreloadcog.error
async def reloaderror(ctx, error):
  await ctx.channel.send(f"`ERROR` : `{error}`")

#-------------------------------------------------------------dev cmds end


bot.remove_command('help')
# help_pages


# events


@bot.event
async def on_ready():
    UPTIME_DICT["uts"] = str(int(time.time()))
    change_status.start()
    print(f'logged in as {bot.user}')


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.channel.send(f"{error}\n type ethelp for a list of commands")
#     else:
#         await ctx.channel.send(error)

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
            await c.send("**Thanks you for inviting me!!**\n**My prefix is ** `et`\ntype `ethelp` to get a list of commands!!\nMake sure i have send message, embed links and add reaction permission in the channel you want to use the commands!")
            break
        except:
            pass


@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(878420596168462386)
    name = guild.name
    await channel.send(f"Left {name} : {guild.id}")


# tasks ----->>>
@tasks.loop(seconds=30)
async def change_status():
    ran = random.randint(1, 3)
    if ran == 1:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"ethelp || {len(bot.guilds)} servers "))
    if ran == 2:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"ethelp || ping: {round(bot.latency*1000)} ms"))
    if ran == 3:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="ethelp || Version 1.0"))


# commands


@bot.command()
async def vote(ctx):
    await ctx.channel.send("Vote me to support and encourage my developer!\nlink: https://top.gg/bot/875861419801862165/vote/")
    time.sleep(5)
    


@bot.command()
async def emoji(ctx, emo: discord.PartialEmoji):
    url = emo.url
    name = f"`name:` **{emo.name}**"
    t = f"`created at:` <t:{int(emo.created_at.timestamp())}>"
    emid = f"`id:` {emo.id}"
    text = f"{name}\n{emid}\n{t}"
    await ctx.channel.send(text)

    await ctx.channel.send(url)


@emoji.error
async def emoji_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandError):
        emob = discord.Embed(
            title="`Correct syntax:` etemoji <emoji>  ", color=0x00FFFF)
        await ctx.channel.send(embed=emob, delete_after=5)


@bot.command(aliases=["addlink"])
@commands.guild_only()
@commands.has_permissions(manage_emojis=True)
@commands.bot_has_permissions(manage_emojis=True)
async def addurl(ctx, url: str, name: str = None):
    aurl = url
    if not name:
        naam = f"et_emoji{random.randint(1,500)}"
    else:
        naam = name
    async with aiohttp.ClientSession() as session:
        async with session.get(aurl) as response:
            img = await response.read()
    cm = await ctx.guild.create_custom_emoji(name=naam, image=img)
    cem = bot.get_emoji(cm.id)
    await ctx.channel.send(f"Successfully created the emoji {cem}")
    colch = bot.get_channel(885013467587825686)
    await colch.send(f"Added {cem} in server :{ctx.guild.name} with id {ctx.guild.id}\nEmoji name : `{cem.name}`\n{cem.url}")


@addurl.error
async def addurl_error(ctx, error):
    if isinstance(error, discord.ext.commands.NoPrivateMessage):
        await ctx.channel.send("**This command is only executable in server channels!!**")

    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.channel.send(f"{ctx.author.mention} You need `manage_emojis` permission to use this command!")
    elif isinstance(error, discord.ext.commands.BotMissingPermissions):
        await ctx.channel.send("Please make sure I have the `Manage Emojis` permission!")

    else:
        await ctx.channel.send(f"`ERROR`: {error}")


@bot.command(aliases=["addimg", "addf"])
@commands.guild_only()
@commands.has_permissions(manage_emojis=True)
@commands.bot_has_permissions(manage_emojis=True)
async def addfile(ctx, name=None):
    try:
        async with ctx.channel.typing():
            attach = str(ctx.message.attachments[0])
            if not name:
                name = f"et_emoji{random.randint(1,100)}"
            async with aiohttp.ClientSession() as session:
                async with session.get(attach) as response:
                    img = await response.read()
            cm = await ctx.guild.create_custom_emoji(name=name, image=img)
            cem = bot.get_emoji(cm.id)
            await ctx.channel.send(f"Successfully created the emoji {cem}")
            colch = bot.get_channel(885013467587825686)
            await colch.send(f"Added {cem} in server :{ctx.guild.name} with id {ctx.guild.id}\nEmoji name : `{cem.name}`\n{cem.url}")
    except IndexError:
        await ctx.channel.send("Please provide a valid image or gif file")
    except Exception as e:
        await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}')


@addfile.error
async def addfile_error(ctx, error):
    if isinstance(error, discord.ext.commands.NoPrivateMessage):
        await ctx.channel.send("**This command is only executable in server channels!!**")

    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.channel.send(f"{ctx.author.mention} You need `manage_emojis` permission to use this command!")
    elif isinstance(error, discord.ext.commands.BotMissingPermissions):
        await ctx.channel.send("Please make sure I have the `Manage Emojis` permission!")
    elif isinstance(error, discord.ext.commands.CommandError):
        await ctx.channel.send(f"`ERROR` : {error}")


@bot.command(aliases=["create"])
@commands.guild_only()
@commands.has_permissions(manage_emojis=True)
@commands.bot_has_permissions(manage_emojis=True)
async def add(ctx, emo: discord.PartialEmoji, *, naam: str = None):

    url = f"{emo.url}"
    if not naam:
        naam = emo.name

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img = await response.read()
    cm = await ctx.guild.create_custom_emoji(name=naam, image=img)
    cem = bot.get_emoji(cm.id)
    await ctx.channel.send(f"Successfully created the emoji {cem}")
    colch = bot.get_channel(885013467587825686)
    await colch.send(f"Added {cem} in server :{ctx.guild.name} with id {ctx.guild.id}\nEmoji name : `{cem.name}`\n{cem.url}")


@add.error
async def add_error(ctx, error):
    if isinstance(error, discord.ext.commands.NoPrivateMessage):
        await ctx.channel.send("**This command is only executable in server channels!!**")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.channel.send(f"{ctx.author.mention} You need the `manage emojis` permission to execute this command!", delete_after=5)
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.channel.send("Please put an emoji after `etadd` \n(name is optional)")
    elif isinstance(error, discord.ext.commands.BotMissingPermissions):
        await ctx.channel.send(f"{bot.user.mention} needs `Manage Emojis` permission to execute this command!")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.channel.send("**Please put an emoji after **`etadd`\n example: `etadd <emoji> emoji_name`(name is optional)")
    else:
        await ctx.channel.send(f"`ERROR`: {error}")


@bot.command(aliases=['addm', 'createmany'])
@commands.guild_only()
@commands.has_permissions(manage_emojis=True)
@commands.bot_has_permissions(manage_emojis=True)
async def addmany(ctx, emojis: commands.Greedy[discord.PartialEmoji]):
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
            colch = bot.get_channel(885013467587825686)
            await colch.send(f"Added these  {emojilist} in server :{ctx.guild.name} with id {ctx.guild.id}")
        elif len(emojilist) == 0:
            await ctx.channel.send(f"Hey, maybe you forgot to put spaces between the emojis!Try again!!")


@addmany.error
async def addmany_error(ctx, error):
    if isinstance(error, discord.ext.commands.NoPrivateMessage):
        await ctx.channel.send("**This command is only executable in server channels!!**")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.channel.send(f"{ctx.author.mention} You need the `manage emojis` permission to execute this command!", delete_after=15)
    elif isinstance(error, discord.ext.commands.BotMissingPermissions):
        await ctx.channel.send(f"{bot.user.mention} needs `Manage Emojis` permission to execute this command!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.channel.send("**Please put emojis after** `etaddmany`")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.channel.send("**Please put emojis after ** `etaddmany`")
    else:
        await ctx.channel.send(f"`ERROR:` {error}")


@bot.command(aliases=['delm'])
@commands.guild_only()
@commands.has_permissions(manage_emojis=True)
@commands.bot_has_permissions(manage_emojis=True)
async def deletemany(ctx, emojis: commands.Greedy[discord.Emoji]):
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
async def deletemany_error(ctx, error):
    if isinstance(error, discord.ext.commands.NoPrivateMessage):
        await ctx.channel.send("**This command is only executable in server channels!!**")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.channel.send(f"{ctx.author.mention} You need the `manage emojis` permission to execute this command!", delete_after=15)
    elif isinstance(error, discord.ext.commands.BotMissingPermissions):
        await ctx.channel.send(f"{bot.user.mention} needs `Manage Emojis` permission to execute this command!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.channel.send("**Please put emojis after** `etdeletemany`")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.channel.send("**Please put emojis after ** `etdeletemany`")


@bot.command(aliases=['remove', 'del'])
@commands.guild_only()
@commands.has_permissions(manage_emojis=True)
@commands.bot_has_permissions(manage_emojis=True)
async def delete(ctx, emo: discord.Emoji):
    emoname = emo.name
    await emo.delete()
    await ctx.channel.send(f"Deleted emoji {emoname}")


@delete.error
async def delete_error(ctx, error):
    if isinstance(error, discord.ext.commands.NoPrivateMessage):
        await ctx.channel.send("**This command is only executable in server channels!!**")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.channel.send(f"{ctx.author.mention} You need the `manage emojis` permission to execute this command!", delete_after=15)
    elif isinstance(error, discord.ext.commands.BotMissingPermissions):
        await ctx.channel.send(f"{bot.user.mention} needs `Manage Emojis` permission to execute this command!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.channel.send("**Please put an emoji after** `etdelete` to delete the emoji\nExample: `etdelete <emoji_to_be_deleted> `")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.channel.send("**Please put an emoji after ** `etdeletemany` to delete!")


@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_emojis=True)
@commands.bot_has_permissions(manage_emojis=True)
async def rename(ctx, emoji: discord.Emoji, name):
    emid = emoji.id
    await emoji.edit(name=name)
    em = bot.get_emoji(emid)
    await ctx.channel.send(f"Renamed the emoji {str(em)} to {name}")


@rename.error
async def rename_error(ctx, error):
    if isinstance(error, discord.ext.commands.NoPrivateMessage):
        await ctx.channel.send("**This command is only executable in server channels!!**")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.channel.send(f"{ctx.author.mention} You need the `manage emojis` permission to execute this command!", delete_after=15)
    elif isinstance(error, discord.ext.commands.BotMissingPermissions):
        await ctx.channel.send(f"{bot.user.mention} needs `Manage Emojis` permission to execute this command!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.channel.send("**Please put an emoji and the name after **`etrename`** to rename**\nExample: `etrename <emoji> new_name `")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.channel.send("**Please put an emoji and the name after **`etrename`** to rename**\nExample: `etrename <emoji> new_name `")


@bot.command()
@commands.guild_only()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(manage_emojis=True)
async def lock(ctx, emoji: discord.Emoji, role: commands.Greedy[discord.Role]):
    emo = str(emoji)
    sr = discord.utils.get(ctx.guild.roles, name='Emoji Tools')
    role.append(sr)

    await emoji.edit(roles=role)
    rolelist = []
    for i in role:
        t = f"{i.mention}"
        rolelist.append(t)

    em = discord.Embed(
        title=f"**__Successfully locked__** {emo}", description=f"*Only these roles can access this emoji:*\n\n{rolelist}\n\n\nTo unlock:\ntype: `etunlock` {emo}")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Locked by {ctx.author}")
    await ctx.channel.send(embed=em)


@lock.error
async def lock_error(ctx, error):
    if isinstance(error, discord.ext.commands.NoPrivateMessage):
        await ctx.channel.send("**This command is only executable in server channels!!**")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.channel.send(f"{ctx.author.mention} You need the `administrator` permission to execute this command!!")
    elif isinstance(error, discord.ext.commands.BotMissingPermissions):
        await ctx.channel.send(f"{bot.user.mention} needs `Manage Emojis` permission to execute this command!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.channel.send("**Error executing command**!!\nCorrect way: `etlock <emoji> <@roles>`")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.channel.send("Missing required arguments! see `ethelp lock` for more")


@bot.command()
@commands.guild_only()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(manage_emojis=True)
async def unlock(ctx, emoji: discord.Emoji):
    emo = str(emoji)
    await emoji.edit(roles=[ctx.guild.default_role])
    await ctx.channel.send(f"unlocked {emo} for everyone")


@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error, discord.ext.commands.NoPrivateMessage):
        await ctx.channel.send("**This command is only executable in server channels!!**")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.channel.send(f"{ctx.author.mention} You need the `administrator` permission to execute this command!!")
    elif isinstance(error, discord.ext.commands.BotMissingPermissions):
        await ctx.channel.send(f"{bot.user.mention} needs `Manage Emojis` permission to execute this command!")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.channel.send("**Error executing command**!!\nCorrect way: `etunlock <emoji>`")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.channel.send("Missing required arguments! see `ethelp unlock` for more")
# ----------- help command


@bot.group(invoke_without_command=True)
async def help(ctx):
    emj = str(bot.get_emoji(876471574037942342))
    emmd = str(bot.get_emoji(876471321301774386))
    embh = discord.Embed(
        title='Help Embed`', description=f'\n\nN.B: All the commands are case sensitive.\n{emj} - Public commands\n{emmd} - Moderator/Admin commands\n', color=0xFF657F)

    emb2 = discord.Embed(
        title='Help Embed', description=f'\n\nN.B: All the commands are case sensitive.\n{emj} - Public commands\n{emmd} - Moderator/Admin commands\n', color=0xFF657F)
    embh.add_field(
        name=f"{emj} emoji", value='`etemoji <emoji>`\nShows information about the emoji and sends an image object of the emoji!')
    embh.add_field(
        name=f"{emmd} add", value='`etadd <emoji> [name(optional)]`\nCreates a custom emoji in the guild form external servers!`(You need nitro to put external emojis in the command line)`')

    embh.add_field(
        name=f'{emmd} rename', value="`etrename <emoji> <new_name>`\nRenames an emoji!")

    embh.add_field(name=f"{emmd} delete",
                   value='`etdelete <emoji>`\n Deletes an emoji')

    embh.add_field(
        name=f"{emmd} addurl", value="`etaddurl <image_url> <optional_name>`\nCreates an emoji from the provided image url or gif as discord attachment link!!\n You must use a discord attachment url!")
    embh.add_field(name=f"{emmd} addfile",
                   value="`etaddfile [optional_name] <image_attachment>`\nCreates an emoji from the provided attachment, Note that the file size can't exceed 256.0 kb")
    embh.add_field(name=f'{emmd} addmany',
                   value=f'`etaddmany <emoji> <emoji> ....`\nCreates multiple custom emojis at once!!(`currently upto 5 emojis at once`).You must put spaces between the emojis!!`(! can not use without nitro)`', inline=False)
    embh.add_field(name=f"{emmd} deletemany",
                   value='`etdeletemany <emoji> <emoji> .....`\n Deletes multiple emojis at once(`currently upto 5 emojis at once`). You must put spaces between the emojis!!', inline=False)
    embh.add_field(name="**Useful Links**",
                   value="[vote](https://top.gg/bot/875861419801862165/vote/) | [invite](https://discord.com/api/oauth2/authorize?client_id=875861419801862165&permissions=1074121792&scope=bot) | [support server](https://discord.gg/zZPf2BUkHm)", inline=False)
    emb2.add_field(
        name=f"{emmd} lock", value='`etlock <emoji> <role> <role> ....`\nLocks the emoji to only the mentioned roles!\n`make sure you put spaces between etlock and the emoji and the roles `')
    emb2.add_field(
        name=f"{emmd} unlock", value='`etlock <emoji>`\nUnlocks the emoji for everyone!!')
    emb2.add_field(name=f"{emj} ping",
                   value="`etping`\nTo see the bot's latency in ms")
    emb2.add_field(
        name=f"{emj} botinfo", value="`etbotinfo`\nShows information about the bot!also provides a link of the support server invite!!")
    emb2.add_field(
        name=f"{emj} invite", value="`etinvite`\nSends the OAuth url to invite the bot!!")
    emb2.add_field(
        name=f"{emj} count", value="`etcount`\n Counts the maximum capacity of emoji slots in a server and total number of used slots!")
    emb2.add_field(name="**Useful Links**",
                   value="[vote](https://top.gg/bot/875861419801862165/vote/) | [invite](https://discord.com/api/oauth2/authorize?client_id=875861419801862165&permissions=1074121792&scope=bot) | [support server](https://discord.gg/zZPf2BUkHm)", inline=False)
    embh.set_footer(icon_url=bot.user.avatar_url,
                    text=f"Page 1/2 |use ethelp [command_name] to get more information!")
    emb2.set_footer(icon_url=bot.user.avatar_url,
                    text=f"Page 2/2 |use ethelp [command_name] to get more information!")
    bot.help_pages = [embh, emb2]

    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
    current = 0
    msg = await ctx.channel.send(embed=bot.help_pages[current])
    for button in buttons:
        await msg.add_reaction(button)
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
        except asyncio.TimeoutError:
            for button in buttons:
                await msg.remove_reaction(button, bot.user)
        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0

            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1

            elif reaction.emoji == u"\u27A1":
                if current < len(bot.help_pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(bot.help_pages)-1

            if current != previous_page:
                await msg.edit(embed=bot.help_pages[current])


@help.error
async def help_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandError):
        try:
            await ctx.channel.send(f"Please make sure {bot.user.mention} has `embed links` permission in this channel in order to send the embedded help message!")
        except:
            mm = ctx.author
            await mm.send(f"Please make sure {bot.user.mention} has `embed links` and `send message` permission in the channel in order to send the embedded help message!")


@help.command()
async def emoji(ctx):
    emj = str(bot.get_emoji(876471574037942342))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f'{emj} emoji', description="Shows the name, id, and time of creation of a emoji!\nAlso sends the url of the emoji so you can download or share it\n[Example](https://media.discordapp.net/attachments/875442571181195265/883772917295489084/Screenshot_20210904-235745_Discord_1.jpg)", color=0x90EE90)
    em.add_field(name=f'{alert}Syntax:', value="**etemoji <emoji>**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@help.command()
async def lock(ctx):
    emj = str(bot.get_emoji(876471321301774386))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f"{emj} lock", description="Locks an emoji so that only the specified roles can access it! Only Admins can use this command!! Make sure you mention your role so you can unlock it later!\n [Example](https://cdn.discordapp.com/attachments/883769510711136276/883776523881041950/Screenshot_20210905-001138_Discord_1.jpg)", color=0x90EE90)
    em.add_field(name=f"{alert} Syntax:",
                 value="**etlock <emoji> @role @role .... @role**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@help.command()
async def unlock(ctx):
    emj = str(bot.get_emoji(876471321301774386))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f"{emj} unlock", description="Unlocks an emoji for everyone that was locked before!\n [Example](https://cdn.discordapp.com/attachments/883769510711136276/883776736041533520/Screenshot_20210905-001254_Discord_1.jpg)", color=0x90EE90)
    em.add_field(name=f"{alert} Syntax:", value="**etunlock <emoji>**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@help.command()
async def add(ctx):
    emj = str(bot.get_emoji(876471321301774386))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f"{emj} add", description="Creates a custom emoji in the server! Takes an external emoji as arguement and a name as an optional arguement.\n[Example](https://media.discordapp.net/attachments/875442571181195265/883771679430553640/Screenshot_20210904-235154_Discord_1.jpg)", color=0x90EE90)
    em.add_field(name=f"{alert} Syntax:", value="**etadd <emoji>**")
    em.add_field(name=f"{alert} Aliases:", value="**create**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@help.command()
async def addurl(ctx):
    emj = str(bot.get_emoji(876471321301774386))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f"{emj} addurl", description="Creates an emoji from the image url or gif url(must be discord attachment url) provided!!\n [Example](https://cdn.discordapp.com/attachments/883769510711136276/883775122027212830/Screenshot_20210905-000624_Discord_1.jpg)", color=0x90EE90)
    em.add_field(name=f"{alert} Syntax:",
                 value="**etaddurl <image_url> <optional_name>**")
    em.add_field(name=f"{alert} Aliases:", value="**addlink**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@help.command()
async def addfile(ctx):
    emj = str(bot.get_emoji(876471321301774386))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f"{emj} addfile", description="Creates an emoji from the image attachment. ! **the attachment file size can't be more than 256.0 kb**\n[Example](https://cdn.discordapp.com/attachments/875442571181195265/883769396185673779/Screenshot_from_2021-09-04_23-43-46.png)", color=0x90EE90)
    em.add_field(name=f"{alert} Syntax:",
                 value="**etaddfile <optional_name> <file_attachment>**")
    em.add_field(name=f"{alert} Aliases:", value="**addimg**\n**addf**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@help.command()
async def addmany(ctx):
    emj = str(bot.get_emoji(876471321301774386))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f"{emj} addmany", description="Creates multiple emojis at once (`currently upto 5 emojis only`). Takes multiple emojis as arguments. Make sure you put spaces between!\n [Example](https://cdn.discordapp.com/attachments/883769510711136276/883774611655893052/Screenshot_20210905-000428_Discord_1.jpg)", color=0x90EE90)
    em.add_field(name=f"{alert} Syntax:",
                 value="**etaddmany <emoji> <emoji> .....<emoji>**")
    em.add_field(name=f"{alert} Aliases:", value="**addm**\n**createmany**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@help.command()
async def delete(ctx):
    emj = str(bot.get_emoji(876471321301774386))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f"{emj} delete", description="Deletes an emoji from the server! [Example](https://media.discordapp.net/attachments/875442571181195265/883772377849282570/Screenshot_20210904-235528_Discord_1.jpg)", color=0x90EE90)
    em.add_field(name=f"{alert} Syntax:", value="**etdelete <emoji>**")
    em.add_field(name=f"{alert} Aliases:", value="**del**\n**remove**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@help.command()
async def deletemany(ctx):
    emj = str(bot.get_emoji(876471321301774386))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f"{emj} deletemany", description="Deletes multiple emojis at once(`currently upto 5 emojis at once`).  Takes multiple emojis as arguments. Make sure you put spaces between!\n [Example](https://media.discordapp.net/attachments/875442571181195265/883774198680522802/Screenshot_20210905-000222_Discord_1.jpg)", color=0x90EE90)
    em.add_field(name=f"{alert} Syntax:",
                 value="**etdeletemany <emoji> <emoji> .....<emoji>**")
    em.add_field(name=f"{alert} Aliases:", value="**delm**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@help.command()
async def rename(ctx):
    emj = str(bot.get_emoji(876471321301774386))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f"{emj} rename", description="Renames an emoji! Make sure you use '_' instead of spaces between the words!Otherwise only the first word will be taken!\n [Example](https://media.discordapp.net/attachments/875442571181195265/883773485304938526/Screenshot_20210904-235958_Discord_1.jpg)", color=0x90EE90)
    em.add_field(name=f"{alert} Syntax:",
                 value="**etemoji <emoji> <new_name>**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@bot.command()
async def invite(ctx):
    await ctx.channel.send("https://discord.com/api/oauth2/authorize?client_id=875861419801862165&permissions=1074121792&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D875861419801862165%26permissions%3D1074064448%26scope%3Dbot&scope=bot%20applications.commands")


@help.command()
async def botinfo(ctx):
    emj = str(bot.get_emoji(876471574037942342))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f'{emj} botinfo', description="Shows the information about the bot! and a link to the support server!", color=0x90EE90)
    em.add_field(name=f'{alert}Syntax:', value="**etbotinfo**")
    em.add_field(name=f"{alert} Aliases:", value="**info**\n")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@help.command()
async def invite(ctx):
    emj = str(bot.get_emoji(876471574037942342))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f'{emj} invite', description="Sends the Oauth url to invite the bot!", color=0x90EE90)
    em.add_field(name=f'{alert}Syntax:', value="**etinvite**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@help.command()
async def count(ctx):
    emj = str(bot.get_emoji(876471574037942342))
    alert = str(bot.get_emoji(876470355894620160))
    em = discord.Embed(
        title=f'{emj} count', description="Counts how many emoji a server can have and how many slots have been occupied!", color=0x90EE90)
    em.add_field(name=f'{alert}Syntax:', value="**etcount**")
    em.add_field(name=f"{alert} Aliases:",
                 value="**serverstats**\n**emojicount**\n**emotescount**")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@bot.command(aliases=["emojicount", "emotescount", "count"])
async def serverstats(ctx):
    mcount = ctx.guild.emoji_limit
    ucount = len(ctx.guild.emojis)
    await ctx.channel.send(f"This server can have upto {mcount*2} custom emojis.\n{ucount} slots have been used!!")
    if ucount > mcount*2:
        un = ucount - mcount*2
        await ctx.channel.send(f"However, `{un}` emojis are unavailable due to low boosting level!")


@bot.command(aliases=['info'])
async def botinfo(ctx):
    bug = str(bot.get_emoji(876477723491582042))
    dev = str(bot.get_emoji(879333133617614858))
    the_owner = bot.get_user(428812756456570882)
    ts = int(UPTIME_DICT["uts"])

    em = discord.Embed(title="**Emoji Tools**",
                       description="Emoji Tools is made on the purpose to help you manage emojis in your server!", color=0x90EE00)
    em.add_field(name="**Info**",
                 value=f"`Bot created` : <t:{int(bot.user.created_at.timestamp())}:F>\n`Uptime` : since <t:{ts}:R>\n`Servers` : {len(bot.guilds)} servers\n`Users` : {len(bot.users)} users afaics\n", inline=False)
    em.add_field(name=f'{bug}Support server:',
                 value="Join the support server if you encounter any error while using the bot.\n https://discord.gg/zZPf2BUkHm")

    em.add_field(name=f"{dev} Developer Info.",
                 value=f"{the_owner.mention} -> Owner and Developer")
    em.set_footer(icon_url=ctx.author.avatar_url,
                  text=f"Requested by {ctx.author}")
    await ctx.channel.send(embed=em)


@bot.command()
async def ping(ctx):
    title = f"PING : ***{round(bot.latency*1000)} ms***  "
    embed = discord.Embed(title=title, color=0x00FFFF)
    await ctx.channel.send(embed=embed)


@bot.command()
async def stats(ctx):
    servercount = len(bot.guilds)
    membercount = 0
    emojicount = 0

    for i in bot.guilds:
        e = len(i.emojis)
        emojicount += e
        x = i.member_count
        membercount += x
    await ctx.channel.send(f"**__Server Count:__**\n{servercount} servers\n**__Total members:__**\n{membercount} members\n**__Total Emojis__:**\n{emojicount} Emojis")


@bot.command()
async def slist(ctx):
    if ctx.author.id == 428812756456570882:
        servers = []
        c = 0
        for i in bot.guilds:

            servers.append(i.name)
            c += 1
        await ctx.channel.send(f"Total {c} servers!\n{servers}")


# dev commands

@bot.command()
async def getsid(ctx, *, name: str):
    if ctx.author.id == 428812756456570882:
        s = discord.utils.get(bot.guilds, name=name)
        sid = str(s.id)
        await ctx.reply(sid)


@bot.command(aliases=['dsi'])
async def devserverinfo(ctx, sid):
    if ctx.author.id == 428812756456570882:
        server_id = int(sid)
        server = bot.get_guild(server_id)
        await ctx.send(f"**{server.name}**\nmembers :{server.member_count}\nemojis: {len(server.emojis)}")





@bot.command(aliases=['dsl'])
async def devserverleave(ctx, sid):
    if ctx.author.id == 428812756456570882:
        server_id = int(sid)

        server = bot.get_guild(server_id)

        name = server.name
        await server.leave()
        await ctx.send(f"left the server {name}")

bot.run(TOKEN)
