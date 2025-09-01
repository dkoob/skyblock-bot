import discord
from os import getenv
from discord import app_commands
from discord.ext import commands
from typing import Literal
import random
import asyncio

from utilities.embedhandler import EmbedHandler

GUILD_ID = getenv("DEV_SERVER_ID")

EMOJI_MAGICFIND = "<:magicfind:1410010455178739904>"
EMOJI_BOOK = "<:enchantedbook:1411069906484461760>"
EMOJI_PETLUCK = "<:petluck:1411068693051473961>"
EMOJI_HCDICE = "<:hcdice:1411069369542250727>"


class Dice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Dice cog loaded and ready.")

    @app_commands.command(name="roll", description="Try your luck.")
    async def roll(self, interaction: discord.Interaction, highclass: bool = False):
        if highclass:
            odds = 16
            DICE_EMOJI = EMOJI_HCDICE
        else:
            odds = 24

        first_embed = EmbedHandler.new(
            title=f"{EMOJI_HCDICE} Rolling...",
            description=f"",
            embed_type="general"
        )

        await interaction.response.send_message(embed=first_embed)

        await asyncio.sleep(3)

        result = random.randint(1, odds)

        if result == 6:
            DICE_RESULT = "https://cdn.discordapp.com/attachments/1305625750996516938/1411444756424298638/image.png?ex=68b4addd&is=68b35c5d&hm=658db8ebce180d00723dc667ea3b0f35a54b1cef814d7e8b8f70f7f5681992a9&"
        elif result != 6:
            displayed_image = random.randint(1, 5)
            if displayed_image == 1:
                DICE_RESULT = "https://cdn.discordapp.com/attachments/1305625750996516938/1411446487833116783/image.png?ex=68b4af7a&is=68b35dfa&hm=dd9299923f44b83774f0a9931b08b99a712e612fdb53bede1a559eda1ab5f329&"
            elif displayed_image == 2:
                DICE_RESULT = "https://cdn.discordapp.com/attachments/1305625750996516938/1411446636839964672/image.png?ex=68b4af9d&is=68b35e1d&hm=61158eddaf366bd7bd5b3bd064d4b2b09719a662e7b138f757a8ec12c0c38de0&"
            elif displayed_image == 3:
                DICE_RESULT = "https://cdn.discordapp.com/attachments/1305625750996516938/1411446784147849407/image.png?ex=68b4afc0&is=68b35e40&hm=171a9d3f03c1f35aface30e2341e3c23cf1143fb4e162c14d2d034d5d11bb142&"
            elif displayed_image == 4:
                DICE_RESULT = "https://cdn.discordapp.com/attachments/1305625750996516938/1411446947855990965/image.png?ex=68b4afe7&is=68b35e67&hm=0536af38ceef22481096aed5018cb3523a9a301bf0e300a33a98facedc6e5dd6&"
            elif displayed_image == 5:
                DICE_RESULT = "https://cdn.discordapp.com/attachments/1305625750996516938/1411447033318871051/image.png?ex=68b4affc&is=68b35e7c&hm=63611a639ab08679e92729ed5ebd23e9e3ea6c0b38359b1e5ac27f941fbfaf1b&"

        result_embed = EmbedHandler.new(
            embed_type="general",
            image=DICE_RESULT
        )

        await interaction.edit_original_response(embed=result_embed)

async def setup(bot: commands.Bot):
    cog = Dice(bot)
    await bot.add_cog(cog)

    guild_obj = discord.Object(id=GUILD_ID)
    bot.tree.add_command(cog.roll, guild=guild_obj)