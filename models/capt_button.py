

import discord
from discord import ui
from config.settings import CAPT_CHANNEL_ID, ADMIN_ROLE_ID, CATEGORY_ID


# 1. Модальное окно (появляется после нажатия кнопки)
class CreatingChats(ui.Modal, title='Создание чата для откатов'):
    channel_name = ui.TextInput(
        label="Название канала",
        placeholder="откат",
        min_length=3,
        max_length=30
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = guild.get_channel(CATEGORY_ID)
        admin_role = guild.get_role(ADMIN_ROLE_ID)

        if category is None:
            return await interaction.response.send_message("Ошибка: Категория не найдена", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel = await guild.create_text_channel(
            name=self.channel_name.value,
            category=category,
            overwrites=overwrites
        )

        await channel.send(
            f"Привет {interaction.user.mention}! Присылай откаты. {admin_role.mention if admin_role else ''}"
            f"{admin_role.mention if admin_role else ''} <@&{ADMIN_ROLE_ID}>")

        await interaction.response.send_message(f"Чат создан: {channel.mention}", ephemeral=True)


# 2. Класс кнопки (который бот отправит в канал)
class CaptApplicationButton(ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # timeout=None важен для вечной работы

    @ui.button(label="Создать чат для откатов", style=discord.ButtonStyle.primary, custom_id="create_capt_btn")
    async def capt_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(CreatingChats())



