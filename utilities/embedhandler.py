import discord
from datetime import datetime

class EmbedHandler:

    EMBED_TYPES = {
        "system": "222222",
        "general": "0059b2",
    }

    FOOTER_TYPES = {
        "system": "This is a System Command • /help • {time}",
        "general": "Having any issues with the bot? • dm @dk.y or @fairi. • {time}",
    }

    DEFAULT_TYPE = "general"
    LOGO_URL = "https://cdn.discordapp.com/attachments/1411102050300727396/1411102078314614804/image.png?ex=68b36eb8&is=68b21d38&hm=7328b9261854e919edeb07ff23ae18d551faee27a5ce13b0870348fd056050de&"

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

        embed.set_footer(text=footer_text, icon_url=EmbedHandler.LOGO_URL)
        return embed
