from os import name
import discord
from discord.ext import commands
from discord import ui
import typing
import humanize
import time


class PublicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["botinfo", "information", "about"], brief="shows information about the bot .", help="Gives you some information about the bot and the developer.", description="Gives you some information about the bot and the developer.")
    async def info(self, ctx):
        bug = str(self.bot.get_emoji(876477723491582042))
        dev = str(self.bot.get_emoji(879333133617614858))
        
        ts = self.bot.uptime
        delt = int(time.time()) - ts
        users = sum(g.member_count for g in self.bot.guilds)

        em = discord.Embed(title="**Emoji Tools**",
                           description="Emoji Tools is made on the purpose to help you manage emojis in your server!", color=0x2F3136)
        em.add_field(name="**Info**",
                     value=f"`Bot created` : <t:{int(self.bot.user.created_at.timestamp())}:F>\n`Uptime` : Online since <t:{str(ts)}:f> | `{humanize.precisedelta(delt)}`\n`Servers` : {len(self.bot.guilds)} servers\n`Users` : {users} users \n", inline=False)
        em.add_field(name=f'{bug}Support server:',
                     value="Join the support server if you encounter any error while using the bot.\n https://discord.gg/zZPf2BUkHm")

        em.add_field(name=f"{dev} Developer Info.",
                     value=f"SHERLOCK#7309 -> Owner and Developer")
        em.set_footer(text=f"Requested by {ctx.author}")
        view = ui.View()
        b1 = ui.Button(label="Invite", emoji='<:website:877638561501950003>', style=discord.ButtonStyle.green,
                       url="https://discord.com/oauth2/authorize?client_id=875861419801862165&permissions=138513009728&scope=bot%20applications.commands")
        b2 = ui.Button(label="Vote", emoji='<:discordbotlist:880695425710063646>',
                       style=discord.ButtonStyle.green, url="https://top.gg/bot/875861419801862165/vote/")
        b3 = ui.Button(label="Support server", emoji='<:CH_IconBugHunterBadge:876477723491582042>',
                       style=discord.ButtonStyle.green, url="https://discord.gg/zZPf2BUkHm")

        view.add_item(b1)
        view.add_item(b2)
        view.add_item(b3)

        await ctx.channel.send(embed=em, view=view)

    @commands.command(name="invite", aliases=["inv", "addtoserver"], brief="invite link to add **Emoji Tools**", help="OAuth url to invite emoji tools", description="gives you the OAuth url to invite emoji tools")
    async def invite(self, ctx):
        view = ui.View()
        b1 = ui.Button(label="Invite", emoji='<:website:877638561501950003>', style=discord.ButtonStyle.green,
                       url="https://discord.com/oauth2/authorize?client_id=875861419801862165&permissions=138513009728&scope=bot%20applications.commands")
        b2 = ui.Button(label="Vote", emoji='<:discordbotlist:880695425710063646>',
                       style=discord.ButtonStyle.green, url="https://top.gg/bot/875861419801862165/vote/")
        b3 = ui.Button(label="Support server", emoji='<:CH_IconBugHunterBadge:876477723491582042>',
                       style=discord.ButtonStyle.green, url="https://discord.gg/zZPf2BUkHm")

        view.add_item(b1)
        view.add_item(b2)
        view.add_item(b3)
        embed = discord.Embed(title="Invite me! and please vote me too",
                              description="[Emoji Tools](https://discord.com/oauth2/authorize?client_id=875861419801862165&permissions=138513009728&scope=bot%20applications.commands)", color=0x2F3136)
        embed.set_author(icon_url=self.bot.user.avatar.url, name="Emoji Tools")

        await ctx.channel.send(embed=embed, view=view)

    @commands.command(name="support", aliases=["supportserver", "supports", "report"], brief="Invite link to the support server", help="get invite link for the support server to report bugs")
    async def support(self, ctx):
        emby = discord.Embed(title="Support server invite link",
                             description="Join the server and report you issue or bugs.\nhttps://discord.gg/zZPf2BUkHm", color=0x2F3136)

        view = ui.View()
        b1 = ui.Button(label="Support server", emoji='<:CH_IconBugHunterBadge:876477723491582042>',
                       style=discord.ButtonStyle.green, url="https://discord.gg/zZPf2BUkHm")
        b2 = ui.Button(label="Vote", emoji='<:discordbotlist:880695425710063646>',
                       style=discord.ButtonStyle.green, url="https://top.gg/bot/875861419801862165/vote/")
        view.add_item(b1)
        view.add_item(b2)
        await ctx.channel.send(embed=emby, view=view)

    @commands.command(name="vote", aliases=["v", "dblvote"], brief="Vote me to help me grow faster.", help="You can vote me at Top.gg , discordbotlist and in many other botlists.Vote me to get extra neat features.", description="You can vote me at Top.gg, discordbotlist and in many other botlists.Vote me to get extra neat features.")
    async def vote(self, ctx):
        emby = discord.Embed(title="Vote me to support and unlock cool features!",
                             description="**voter perks**: `Emoji Searching(in beta state now)`\nVote me at these sites\n[Top.gg](https://top.gg/bot/875861419801862165/vote/)\n[Bladebotlist](https://bladebotlist.xyz/bot/875861419801862165/vote)\n[DiscordBotlist](https://discordbotlist.com/bots/emoji-tools)\n[Discords.com/bots](https://discords.com/bots/bot/875861419801862165/vote)", color=0x2F3136)
        emby.set_author(icon_url=self.bot.user.avatar.url, name="Emoji Tools")

        view = ui.View()

        b1 = ui.Button(label="Top.gg", emoji='<:discordbotlist:880695425710063646>',
                       style=discord.ButtonStyle.green, url="https://top.gg/bot/875861419801862165/vote/")
        b2 = ui.Button(label="DC bot list", emoji='<:Emoji_tools:883769038600294421>',
                       style=discord.ButtonStyle.green, url="https://discordbotlist.com/bots/emoji-tools")
        b3 = ui.Button(label="Discords.com", emoji='<:Emoji_tools:883769038600294421>',
                       style=discord.ButtonStyle.green, url="https://discords.com/bots/bot/875861419801862165/vote")
        b4 = ui.Button(label="BladeBotlist", emoji='<:Emoji_tools:883769038600294421>',
                       style=discord.ButtonStyle.green, url="https://bladebotlist.xyz/bot/875861419801862165/vote")
        view.add_item(b1)
        view.add_item(b2)
        view.add_item(b3)
        view.add_item(b4)
        await ctx.channel.send(embed=emby, view=view)

    def stat_or_anim(self, guild):
        statc = 0
        animc = 0
        for e in guild.emojis:
            if e.animated:
                animc += 1
            else:
                statc += 1
        return statc, animc

    @commands.command(name="count", aliases=["serverstats", "emojicount", "stickercount"], brief="Shows emoji counts , sticker counts and information about the server's emojis and stickers", help="Shows emoji counts, sticker counts and informations about the server's emojis and stickers. Useful for checking emoji slots and sticker slots.", description="Shows emoji counts, sticker counts and information about the server's emojis. You can check the maximum emoji count/sticker count and how many slots are left .")
    @commands.guild_only()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def count(self, ctx):
        guild = ctx.guild
        max_emojis = guild.emoji_limit  # x2
        max_stickers = guild.sticker_limit
        e_used_slots = len(guild.emojis)
        s_used_slots = len(guild.stickers)
        flag = False
        if e_used_slots >= max_emojis*2:
            unavailable = e_used_slots - max_emojis*2
            flag = True
        statc, animc = self.stat_or_anim(guild)
        embed = discord.Embed(title=f"Emojis and Stickers",
                              color=0x2F3136, timestamp=ctx.message.created_at)
        embed.set_author(icon_url=guild.icon, name=f"{guild.name}")
        embed.add_field(name="<:greentick:880695423516430336> Total slots:",
                        value=f"`Emoji  :` **{max_emojis*2}** slots\n     > {max_emojis} static, {max_emojis} animated\n`Sticker :` **{max_stickers}** slots", inline=False)
        if flag:

            embed.add_field(name="<:greentick:880695423516430336> Used slots:",
                            value=f"`Emoji  :` **{e_used_slots}** slots *({unavailable} unavailable)*\n      >{statc} static emojis\n     >{animc} animated emojis\n`Sticker :` **{s_used_slots}** slots", inline=True)
            embed.add_field(name="<:greentick:880695423516430336> Remaining slots:",
                            value=f"`Emoji  :` No available slots\n`Sticker :` {max_stickers-s_used_slots} slots left", inline=True)
        else:
            embed.add_field(
                name="<:greentick:880695423516430336> Used slots:", value=f"`Emoji  :` **{e_used_slots}** slots\n     >{statc} static\n     >{animc} animated\n`Sticker :` **{s_used_slots}** slots", inline=True)
            embed.add_field(name="<:greentick:880695423516430336> Remaining slots:",
                            value=f"`Emoji  :` **{max_emojis*2 - e_used_slots}** slots left\n     >{max_emojis-statc} static emoji slots left\n     >{max_emojis-animc} animated emoji slots left\n`Sticker :` **{max_stickers-s_used_slots}** slots left", inline=True)

        embed.set_footer(icon_url=self.bot.user.avatar.url, text="Emoji Tools")
        await ctx.send(embed=embed)

    @count.error
    async def count_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("you can't count emojis in a dm, bud")

    @commands.command(name="uptime", aliases=["upt"], brief="Shows bot's uptime", help="Shows bot's uptime", description="Shows bot's uptime")
    async def uptime(self, ctx):
        on_r = self.bot.uptime
        delta = int(time.time()) - on_r
        await ctx.send(f"**{humanize.precisedelta(delta)}**")

    @commands.command(name="ping", aliases=["pong"], hidden=True)
    async def ping(self, ctx):
        title = f"**{round(self.bot.latency*1000)} ms**"
        em = discord.Embed(title=title, color=0x2F3136)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(PublicCog(bot))
