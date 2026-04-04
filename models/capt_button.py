

import discord
from discord import ui
from config.settings import CAPT_CHANNEL_ID, ADMIN_ROLE_ID, CATEGORY_ID, OWNER_ROLE_ID


# Модальное окно
class CaptApplicationButton(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Создать чат для откатов", style=discord.ButtonStyle.primary, custom_id="create_capt_btn")
    async def capt_button(self, interaction: discord.Interaction, button: ui.Button):
        guild = interaction.guild
        category = guild.get_channel(CATEGORY_ID)
        admin_role = guild.get_role(ADMIN_ROLE_ID)

        if not category:
            return await interaction.response.send_message("Ошибка: Категория не найдена", ephemeral=True)

        # Автоназвание по нику
        channel_name = f"откат-{interaction.user.display_name}".lower()

        # Проверка на дубликат
        existing_channel = discord.utils.get(category.text_channels, name=channel_name)
        if existing_channel:
            return await interaction.response.send_message(f"У вас уже есть чат: {existing_channel.mention}", ephemeral=True)

        # Права доступа
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        # Создаем канал
        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        # Отвечаем пользователю
        await interaction.response.send_message(f"Чат создан: {channel.mention}", ephemeral=True)

        # Приветствие в канале
        await channel.send(
            f"Привет {interaction.user.mention}! Этот чат создан специально для твоих откатов.\n"
            f"<@&{ADMIN_ROLE_ID}> <@&{OWNER_ROLE_ID}>"
        )




