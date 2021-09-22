import discord
from discord.ext import commands
from discord import ui
import typing
import humanize,time
class PublicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(name="invite", aliases=["inv", "addtoserver"], brief="invite link to add **Emoji Tools**", help="OAuth url to invite emoji tools", description="gives you the OAuth url to invite emoji tools")
    async def invite(self, ctx):
        view = ui.View()
        b1 = ui.Button(label="Invite", emoji='<:website:877638561501950003>', style=discord.ButtonStyle.green,
                      url="https://discord.com/api/oauth2/authorize?client_id=875861419801862165&permissions=1074121792&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D875861419801862165%26permissions%3D1074064448%26scope%3Dbot&scope=bot%20applications.commands")
        b2 = ui.Button(label="Vote", emoji='<:discordbotlist:880695425710063646>', style=discord.ButtonStyle.green,url="https://top.gg/bot/875861419801862165/vote/")
        b3 = ui.Button(label="Support server", emoji='<:CH_IconBugHunterBadge:876477723491582042>',
                       style=discord.ButtonStyle.green, url="https://discord.gg/zZPf2BUkHm")

        view.add_item(b1)
        view.add_item(b2)
        view.add_item(b3)
        embed = discord.Embed(title="Invite me! and please vote me too", color=0x2F3136)
        embed.set_author(icon_url = self.bot.user.avatar.url, name = "Emoji Tools")

        await ctx.channel.send(embed = embed, view = view)

    @commands.command(name = "support", aliases = ["supportserver", "supports", "report"],brief= "Invite link to the support server", help = "get invite link for the support server to report bugs")
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
        await ctx.channel.send(embed = emby, view = view)
    
    @commands.command(name="info", aliases=["botinfo", "information"], brief="shows information about the bot .", help="Gives you some information about the bot and the developer.", description="Gives you some information about the bot and the developer.")
    async def info(self, ctx):
        bug = str(self.bot.get_emoji(876477723491582042))
        dev = str(self.bot.get_emoji(879333133617614858))
        the_owner = self.bot.get_user(428812756456570882)
        ts = self.bot.uptime
        delt = int(time.time()) - ts

        em = discord.Embed(title="**Emoji Tools**",
                           description="Emoji Tools is made on the purpose to help you manage emojis in your server!", color=0x2F3136)
        em.add_field(name="**Info**",
                    value=f"`Bot created` : <t:{int(self.bot.user.created_at.timestamp())}:F>\n`Uptime` : Online since <t:{str(ts)}:R> | `{humanize.precisedelta(delt)}\n`Servers` : {len(self.bot.guilds)} servers\n`Users` : {len(self.bot.users)} users afaics\n", inline=False)
        em.add_field(name=f'{bug}Support server:',
                    value="Join the support server if you encounter any error while using the bot.\n https://discord.gg/zZPf2BUkHm")

        em.add_field(name=f"{dev} Developer Info.",
                    value=f"{the_owner} -> Owner and Developer")
        em.set_footer(icon_url=ctx.author.avatar.url,
                    text=f"Requested by {ctx.author}")
        view = ui.View()
        b1 = ui.Button(label="Invite", emoji='<:website:877638561501950003>', style=discord.ButtonStyle.green,
                       url="https://discord.com/api/oauth2/authorize?client_id=875861419801862165&permissions=1074121792&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D875861419801862165%26permissions%3D1074064448%26scope%3Dbot&scope=bot%20applications.commands")
        b2 = ui.Button(label="Vote", emoji='<:discordbotlist:880695425710063646>',
                       style=discord.ButtonStyle.green, url="https://top.gg/bot/875861419801862165/vote/")
        b3 = ui.Button(label="Support server", emoji='<:CH_IconBugHunterBadge:876477723491582042>',
                       style=discord.ButtonStyle.green, url="https://discord.gg/zZPf2BUkHm")

        view.add_item(b1)
        view.add_item(b2)
        view.add_item(b3)

        await ctx.channel.send(embed=em, view = view)


def setup(bot):
    bot.add_cog(PublicCog(bot))
