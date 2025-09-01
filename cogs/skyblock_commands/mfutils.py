import discord
import math
from os import getenv
from discord import app_commands
from discord.ext import commands
from typing import Literal

from utilities.embedhandler import EmbedHandler

GUILD_ID = getenv("DEV_SERVER_ID")

EMOJI_MAGICFIND = "<:magicfind:1410010455178739904>"
EMOJI_BOOK = "<:enchantedbook:1411069906484461760>"
EMOJI_PETLUCK = "<:petluck:1411068693051473961>"
EMOJI_HCDICE = "<:hcdice:1411069369542250727>"


class MFutils(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("MFUtils cog loaded and ready.")

    @app_commands.command(name="calculatemf", description="Calculate your magic find.")
    @app_commands.describe(
        magic_find="How much magic find you have.",
        drop_chance="Base chance of dropping the item (for example, 0.5 for 0.5%).",
        looting="Your looting enchantment level (0 for none).",
        pet_luck="How much pet luck you have.",
        luck="Your luck enchantment level (0 for none).",
        drop_type="What type of drop is this?"
    )
    @app_commands.rename(
        magic_find='magicfind',
        drop_chance='dropchance',
        pet_luck='petluck',
        drop_type='droptype'
    )
    async def calculatemf(
        self,
        interaction: discord.Interaction,
        magic_find: float,
        drop_chance: float,
        drop_type: Literal["Normal", "Slayer", "Pet", "Armor"],
        looting: int = 0,
        pet_luck: int = 0,
        luck: int = 0,
    ):
        
        embed = EmbedHandler.new(
            title="Magic Find Calculator",
            description="Calculating...",
            embed_type="general"
        )

        if drop_chance > 5:
            error_embed = EmbedHandler.new(
                title="Error",
                description="This drop is not affected by Magic Find.",
                embed_type="general"
            )
            error_embed.color = discord.Color.red()
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

        stats_text = f" {EMOJI_MAGICFIND}Magic Find: **{int(magic_find)}**\n {EMOJI_HCDICE}Base droprate: **{drop_chance}%**\n {EMOJI_BOOK}Looting level: **{looting}**\n {EMOJI_PETLUCK}Pet Luck: **{pet_luck}**\n {EMOJI_BOOK}Luck: **{luck}**"
        embed.add_field(name="Your Stats", value=stats_text, inline=False)

        
        mf_multiplier = 1 + (magic_find / 100)
        pet_luck_multiplier = 1 + (pet_luck / 100)
        looting_multiplier = 1 + (looting * 0.15)
        luck_multiplier = 1 + (luck * 0.05)

        
        if drop_type == "Pet":
            final_chance = drop_chance * mf_multiplier * pet_luck_multiplier
        elif drop_type == "Armor":
            final_chance = drop_chance * mf_multiplier * luck_multiplier
        elif drop_type == "Slayer":
            final_chance = drop_chance * mf_multiplier
        else: 
            final_chance = drop_chance * mf_multiplier * looting_multiplier

        final_chance = min(final_chance, 100.0)
        
        if final_chance > 0:
            one_in = 1 / (final_chance / 100)
            result_text = f"Your chance to drop this item is **{final_chance:.2f}%**\nThis is approximately **1 in {one_in:,.0f}** drops."
        else:
            result_text = "Your chance to drop this item is **0%**."

        embed.add_field(name="Result", value=result_text, inline=False)

        footer_text = (
            f"hellooo"
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    cog = MFutils(bot)
    await bot.add_cog(cog)

    guild_obj = discord.Object(id=GUILD_ID)
    bot.tree.add_command(cog.calculatemf, guild=guild_obj)