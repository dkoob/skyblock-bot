import discord
from datetime import datetime

class EmbedHandler:

    EMBED_TYPES = {
        "system": "808080",
        "general": "228B22",
    }

    FOOTER_TYPES = {
        "system": "This is a System Command • /help • {time}",
        "general": "Having any issues with the bot? • dm @dk.y or @fairi. • {time}",
    }

    DEFAULT_TYPE = "general"

    @staticmethod
    def new(
            title: str = None,
            description: str = None,
            color: int = None,
            fields: list[tuple[str, str, bool]] = None,  # list of (name, value, inline)
            thumbnail: str = None,
            image: str = None,
            embed_type: str = None,
    ) -> discord.Embed:
        color = EmbedHandler.EMBED_TYPES.get(embed_type, EmbedHandler.EMBED_TYPES[EmbedHandler.DEFAULT_TYPE])
        footer_template = EmbedHandler.FOOTER_TYPES.get(embed_type, EmbedHandler.FOOTER_TYPES[EmbedHandler.DEFAULT_TYPE])
        now = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        footer_text = footer_template.format(time=now)
        embed = discord.Embed(
            title=title,
            description=description,
            color= int(color, 16),
        )

        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        if image:
            embed.set_image(url=image)

        embed.set_footer(text=footer_text)
        return embed
