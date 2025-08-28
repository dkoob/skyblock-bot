# General Imports
import os
import logging
import platform

import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv()

class ColorFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    cyan = "\x1b[36m"
    purple = "\x1b[35m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(green){asctime}(reset)  |  (levelcolor){levelname:<8}(reset)  |  (namecolor){name}(reset) - {message}"
        format = format.replace("(green)", self.green + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        # this is a very rough way to do this, but i wanted different colors in the logging messages and didnt feel like doing a whole function for it
        if record.name is not "discord_bot":
            format = format.replace("(namecolor)", self.purple + self.bold)
        else:
            format = format.replace("(namecolor)", self.cyan + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)

color_formatter = ColorFormatter()

def setup_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(color_formatter)
        logger.addHandler(ch)
    logger.propagate = False
    return logger

bot_logger = setup_logger("discord_bot")
discord_loggers = ["discord", "discord.client", "discord.gateway", "discord.ext.commands.bot"]
for name in discord_loggers:
    setup_logger(name)

intents = discord.Intents.default()

class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("/"),
            intents=intents,
            help_command=None,
        )

        self.logger = bot_logger
        self.database = None
        self.invite_link = os.getenv("INVITE_LINK")

    async def load_cogs(self) -> None:
        cogs_path = os.path.join(os.path.dirname(__file__), "cogs")
        for file in os.listdir(cogs_path):
            if file.endswith(".py") and file != "__init__.py":
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    self.logger.error(f"Failed to load extension {extension}: {type(e).__name__}: {e}")

    async def setup_hook(self) -> None:
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        await self.load_cogs()

    async def on_ready(self):
        if not hasattr(self, "ready_done"):
            self.ready_done = True
            self.logger.info(f"Logged in as {self.user}")
            await self.change_presence(activity=discord.CustomActivity("/help | by @dk.y"))

# ----- this code was fully taken from a template online, ive just added it in cause i intend on recreating it later -----
# async def on_command_completion(self, context: Context) -> None:
#     """
#     The code in this event is executed every time a normal command has been *successfully* executed.
#
#     :param context: The context of the command that has been executed.
#     """
#     full_command_name = context.command.qualified_name
#     split = full_command_name.split(" ")
#     executed_command = str(split[0])
#     if context.guild is not None:
#         self.logger.info(
#             f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
#         )
#     else:
#         self.logger.info(
#             f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
#         )
#
# async def on_command_error(self, context: Context, error) -> None:
#     """
#     The code in this event is executed every time a normal valid command catches an error.
#
#     :param context: The context of the normal command that failed executing.
#     :param error: The error that has been faced.
#     """
#     if isinstance(error, commands.CommandOnCooldown):
#         minutes, seconds = divmod(error.retry_after, 60)
#         hours, minutes = divmod(minutes, 60)
#         hours = hours % 24
#         embed = discord.Embed(
#             description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
#             color=0xE02B2B,
#         )
#         await context.send(embed=embed)
#     elif isinstance(error, commands.NotOwner):
#         embed = discord.Embed(
#             description="You are not the owner of the bot!", color=0xE02B2B
#         )
#         await context.send(embed=embed)
#         if context.guild:
#             self.logger.warning(
#                 f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot."
#             )
#         else:
#             self.logger.warning(
#                 f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot."
#             )
#     elif isinstance(error, commands.MissingPermissions):
#         embed = discord.Embed(
#             description="You are missing the permission(s) `"
#             + ", ".join(error.missing_permissions)
#             + "` to execute this command!",
#             color=0xE02B2B,
#         )
#         await context.send(embed=embed)
#     elif isinstance(error, commands.BotMissingPermissions):
#         embed = discord.Embed(
#             description="I am missing the permission(s) `"
#             + ", ".join(error.missing_permissions)
#             + "` to fully perform this command!",
#             color=0xE02B2B,
#         )
#         await context.send(embed=embed)
#     elif isinstance(error, commands.MissingRequiredArgument):
#         embed = discord.Embed(
#             title="Error!",
#             # We need to capitalize because the command arguments have no capital letter in the code and they are the first word in the error message.
#             description=str(error).capitalize(),
#             color=0xE02B2B,
#         )
#         await context.send(embed=embed)
#     else:
#        raise error

bot = DiscordBot()
bot.run(os.getenv("TOKEN"))
