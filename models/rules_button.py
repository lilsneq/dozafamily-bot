"""Кнопки для правил сервера с большим изображением"""
import discord


class RulesButton(discord.ui.View):
    """Класс для отображения правил с кнопкой-ссылкой"""

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            label='Просмотреть правила сервера',
            style=discord.ButtonStyle.link,
            url='https://docs.google.com/document/d/1eZWV6J8NwFgPeK_vhD6woovznuvxj10Gwcv6-QmnNow/edit?tab=t.0'
        ))

    @classmethod
    async def send_rules(cls, interaction_or_ctx):
        """Метод для удобной отправки сообщения с картинкой и этой кнопкой"""
        url = 'https://i.pinimg.com/1200x/d4/c9/cb/d4c9cbbd34bcb79302cfcd18a5f641fd.jpg'

        embed = discord.Embed(
            title="Правила сервера",
            description="Пожалуйста, ознакомьтесь с правилами нашего сообщества:",
            color=discord.Color.blue()
        )
        embed.set_image(url=url)

        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.send_message(embed=embed, view=cls())
        else:
            await interaction_or_ctx.send(embed=embed, view=cls())


