import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Setup(commands.Cog, name="setup"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @discord.app_commands.command(
        name="sync",
        description="Syncs slash commands.",
    )
    @app_commands.describe(scope="The sync command's scope, can be 'global' or 'guild'")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been synced globally.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been synced in this guild.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.", color=0xE02B2B
        )
        await context.send(embed=embed)

    @discord.app_commands.command(
        name="unsync",
        description="Unsyncs slash commands.",
    )
    @app_commands.describe(
        scope="The sync command's scope, can be 'global' or 'guild'"
    )
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        if scope == "global":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been unsynced globally.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been unsynced in this guild.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.", color=0xE02B2B
        )
        await context.send(embed=embed)

    @discord.app_commands.command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        embed = discord.Embed(description="Shutting down...", color=0xBEBEFE)
        await context.send(embed=embed)
        await self.bot.close()

async def setup(bot) -> None:
    await bot.add_cog(Setup(bot))