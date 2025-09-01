import asyncio
from os import getenv

import discord
from discord.ext import commands
from discord.ui import Button, View

from utilities.embedhandler import *

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
            embed_type="general",
            footer="By @dk.y and @fairi.",
        )
        embed_new = EmbedHandler.new(
            title="Edited Embed!",
            fields=[
                ("Description", f"Hello again, {interaction.user.mention}!", False),
            ],
            embed_type="system",
            footer="I can change the footer too :)",
        )
        async def button_callback(interaction: discord.Interaction):
            await interaction.response.defer()
            await interaction.message.edit(embed=embed_new)
        button = ButtonHandler.new(
            label="Test Button",
            style="success",
            custom_id="test_button",
            callback=button_callback,
            wrap_in_view=True
        )
        await interaction.response.send_message(embed=embed, view=button)

async def setup(bot: commands.Bot):
    cog = Example(bot)
    await bot.add_cog(cog)

    # Register this command only in your guild
    guild_obj = discord.Object(id=GUILD_ID)
    bot.tree.add_command(cog.hello, guild=guild_obj)
