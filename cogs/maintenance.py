import discord
from discord.ext import commands
from __main__ import system_embed_hex
import os

DEV_IDS = [424833537699610634, 257159805070868481]

def is_allowed(ctx):
    return ctx.author.id in DEV_IDS

prefix_check = commands.check(is_allowed)

class Maintenance(commands.Cog, name="maintenance"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(
        name="sync",
        help="Syncs all bot commands globally or in this guild",
    )
    @prefix_check
    async def sync(self, ctx: commands.Context, scope: str) -> None:
        if scope == "global":
            await ctx.bot.tree.sync()
            embed = discord.Embed(
                description="Commands have been synced globally",
                color=int(system_embed_hex, 16),
            )
            await ctx.send(embed=embed)
        elif scope == "guild":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            embed = discord.Embed(
                description="Commands have been synced in this guild only",
                color=int(system_embed_hex, 16),
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="The scope must be `global` or `guild`.",
                color=int(system_embed_hex, 16),
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="unsync",
        help="Unsyncs all bot commands globally or in this guild",
    )
    @prefix_check
    async def unsync(self, ctx: commands.Context, scope: str) -> None:
        if scope == "global":
            for cmd in list(ctx.bot.tree.get_commands(guild=None)):
                ctx.bot.tree.remove_command(cmd.name, guild=None)
            await ctx.bot.tree.sync(guild=None)
            embed = discord.Embed(
                description="Commands have been unsynced globally",
                color=int(system_embed_hex, 16),
            )
            await ctx.send(embed=embed)
        elif scope == "guild":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            embed = discord.Embed(
                description="Commands have been unsynced in this guild only",
                color=int(system_embed_hex, 16),
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="The scope must be `global` or `guild`.",
                color=int(system_embed_hex, 16),
            )
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title="Permission Denied",
                description="You are not allowed to run this command.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            raise error

async def setup(bot) -> None:
    await bot.add_cog(Maintenance(bot))
