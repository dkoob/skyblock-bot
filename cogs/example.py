from os import getenv

import discord
from discord.ext import commands

from utilities.embedhandler import EmbedHandler

GUILD_ID = getenv("DEV_SERVER_ID")

class Example(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Example cog loaded and ready.")

    # Define the command normally
    @discord.app_commands.command(name="hello", description="Say hello to the bot!")
    async def hello(self, interaction: discord.Interaction):
        embed = EmbedHandler.new(
            title="Hello!",
            fields=[
                ("Description", f"Hello, {interaction.user.mention}!", False),
            ],
            embed_type="general"
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    cog = Example(bot)
    await bot.add_cog(cog)

    # Register this command only in your guild
    guild_obj = discord.Object(id=GUILD_ID)
    bot.tree.add_command(cog.hello, guild=guild_obj)
