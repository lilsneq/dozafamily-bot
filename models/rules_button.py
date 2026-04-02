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
        """Метод для удобной отправки сообщения с локальной картинкой и кнопкой"""

        # 1. Создаем объект файла из папки assets
        # Убедитесь, что файл называется именно rules.png
        file = discord.File("assets/rules.jpg", filename="rules.jpg")

        embed = discord.Embed(
            title="Правила сервера",
            description="Пожалуйста, ознакомьтесь с правилами нашего сообщества:",
            color=discord.Color.blue()
        )

        # 2. Привязываем картинку к эмбеду через название файла
        embed.set_image(url="attachment://rules.jpg")

        # 3. Отправляем и файл, и эмбед вместе
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.send_message(file=file, embed=embed, view=cls())
        else:
            await interaction_or_ctx.send(file=file, embed=embed, view=cls())

