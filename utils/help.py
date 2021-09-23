import discord
from discord.ext import commands
from utils import buttons_and_view as bv


class MyHelpCommand(commands.MinimalHelpCommand):
    def __init__(self):

        super().__init__(
            command_attrs={
                'cooldown': commands.CooldownMapping.from_cooldown(1, 3.0, commands.BucketType.member),
                'help': 'Shows help about the bot, a command, or a category',
                'brief': 'run help [command_name] to get more information about the command',
                'aliases': ["commands", "helo", "hel", "hell"],
            }, verify_checks=False, show_hidden=False
        )

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            # Ignore missing permission errors
            if isinstance(error.original, discord.HTTPException) and error.original.code == 50013:
                return

            await ctx.send(str(error.original))

    def get_command_signature(self, command):
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}   "

    async def send_bot_help(self, mapping):
        embed1 = discord.Embed(title="Help page[1/2]", color=0x2F3136, timestamp=self.context.message.created_at,
                               description="```<>          ~ required arguments\n[]          ~ optional arguments\n[emojis]... ~ emojis with spaces between```")
        embed2 = discord.Embed(title="Help page[2/2]", color=0x2F3136, timestamp=self.context.message.created_at,
                               description="```<> ~ required arguments\n[] ~ optional arguments\n[roles]... ~ @roles mentioned with spaces between```")
        # if self.context.author.id == 428812756456570882:
        #     self.show_hidden = True

        c = 0

        for cog, commands in mapping.items():

            filtered = await self.filter_commands(commands)

            command_signatures = [f"{c.name} " + f"{c.brief}\n`" +
                                  self.get_command_signature(c) + "`" for c in filtered]

            cog_name = getattr(cog, "qualified_name", "No Category")

            for cmd in command_signatures:
                if c < 9:
                    embed1.add_field(
                        name=f"<:valid:877700255439798303> {cmd.split(' ',1)[0]}", value=f"{cmd.split(' ',1)[1]}")
                    c += 1
                elif c >= 9:
                    embed2.add_field(
                        name=f"<:valid:877700255439798303> {cmd.split(' ',1)[0]}", value=f"{cmd.split(' ',1)[1]}")

        channel = self.get_destination()
        view = bv.HelpPageButton(self.context, embed1, embed2)
        
        view.page_one.disabled = True

        msg = await channel.send(embed=embed1, view=view)
        view.message = msg
