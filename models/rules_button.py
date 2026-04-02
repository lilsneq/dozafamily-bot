"""Кнопки для правил сервера с большим изображением"""
import discord

class RulesButton(discord.ui.View):
    """Класс для отображения правил с кнопкой-ссылкой"""

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Просмотреть правила сервера', style=discord.ButtonStyle.primary,
                       custom_id="view_rules_btn")
    async def view_rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Здесь вы пишете текст ваших правил"""
        rules_text = (
            "📜 **ПРАВИЛА НАШЕГО СЕРВЕРА**\n\n"
            "1. Ваш текст правила здесь...\n"
            "2. Еще одно правило...\n"
            "3. И так далее...\n\n"
            "Желаем приятной игры!"
        )

        # Отправляем правила только нажавшему (ephemeral=True)
        await interaction.response.send_message(rules_text, ephemeral=True)

    @classmethod
    async def send_rules(cls, interaction_or_ctx):
        """Метод для удобной отправки сообщения с локальной картинкой и кнопкой"""

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

