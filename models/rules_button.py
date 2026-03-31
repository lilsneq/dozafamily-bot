"""Кнопки для правил сервера с большим изображением"""
import discord

class RulesButton(discord.ui.View):
    """Кнопка для показа ссылки на правила с большим изображением"""

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            label='Нажми для просмотра правил',
            style=discord.ButtonStyle.link,
            url='https://i.pinimg.com/1200x/d4/c9/cb/d4c9cbbd34bcb79302cfcd18a5f641fd.jpg'
            # url='https://docs.google.com/document/d/1eZWV6J8NwFgPeK_vhD6woovznuvxj10Gwcv6-QmnNow/'
        ))
