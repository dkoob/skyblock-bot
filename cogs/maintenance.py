import discord
from discord import app_commands
from discord.app_commands import check
from discord.ext import commands
from __main__ import system_embed_hex

def is_owner(interaction: discord.Interaction) -> bool:
    return interaction.user.id == 257159805070868481

class Maintenance(commands.Cog, name="maintenance"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="sync",
        description="Syncs all bot slash commands",
    )
    @discord.app_commands.describe(scope="The sync command's scope, can be 'global' or 'guild'")
    @discord.app_commands.check(is_owner)
    async def sync(self, context: commands.Context, scope: str) -> None:
        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been synced globally",
                color=int(system_embed_hex, 16),
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been synced in this guild only",
                color=int(system_embed_hex, 16),
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.",
            color=int(system_embed_hex, 16),
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unsync",
        description="Unsyncs all bot slash commands",
    )
    @discord.app_commands.describe(scope="The unsync command's scope, can be 'global' or 'guild'")
    @discord.app_commands.check(is_owner)
    async def unsync(self, context: commands.Context, scope: str) -> None:
        if scope == "global":
            for cmd in list(context.bot.tree.get_commands(guild=context.guild)):
                if cmd.cog_name != "Maintenance":
                    context.bot.tree.remove_command(cmd.name, guild=context.guild)
            try:
                await context.bot.tree.sync(guild=context.guild)

            except Exception as e:
                context.bot.logger.error(f"Something went wrong: {type(e).__name__}: {e}")
            embed = discord.Embed(
                description="Slash commands have been unsynced globally",
                color=int(system_embed_hex, 16),
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been unsynced in this guild only",
                color=int(system_embed_hex, 16),
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.",
            color=int(system_embed_hex, 16),
        )
        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Maintenance(bot))