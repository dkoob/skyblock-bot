import discord
from datetime import datetime
from discord.ui import Button

class EmbedHandler:

    EMBED_TYPES = {
        "system": "222222",
        "general": "0059b2",
    }

    FOOTER_TEMPLATES = {
        "system": "This is a System Command • /help • {time}",
        "general": "Having any issues with the bot? • dm @dk.y or @fairi. • {time}",
        "custom": " | {time}",
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
            footer: str = None,
    ) -> discord.Embed:
        color = EmbedHandler.EMBED_TYPES.get(embed_type, EmbedHandler.EMBED_TYPES[EmbedHandler.DEFAULT_TYPE])
        if footer is not None:
            footer_template = footer + EmbedHandler.FOOTER_TEMPLATES.get("custom", EmbedHandler.FOOTER_TEMPLATES[EmbedHandler.DEFAULT_TYPE])
        else:
            footer_template = EmbedHandler.FOOTER_TEMPLATES.get(embed_type, EmbedHandler.FOOTER_TEMPLATES[EmbedHandler.DEFAULT_TYPE])
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

class ButtonHandler:

    STYLE_TYPES = {
        "primary": discord.ButtonStyle.primary,
        "secondary": discord.ButtonStyle.secondary,
        "success": discord.ButtonStyle.success,
        "danger": discord.ButtonStyle.danger,
        "link": discord.ButtonStyle.link,
    }

    @staticmethod
    def new(
            custom_id: str = None,
            disabled: bool = False,
            emoji: str = None,
            label: str = None,
            style: str = "primary",
            url: str = None,
            callback=None,
            wrap_in_view: bool = False,
            timeout: int = 30,
    )   -> discord.ui.Button:
        style_enum = ButtonHandler.STYLE_TYPES.get(style.lower(), discord.ButtonStyle.primary)

        button = discord.ui.Button(
            custom_id=custom_id,
            disabled=disabled,
            emoji=emoji,
            label=label,
            style=style_enum,
            url=url
        )

        if callback:
            button.callback = callback

        if wrap_in_view:
            view = discord.ui.View(timeout=timeout)
            view.add_item(button)
            return button and view

        return button


