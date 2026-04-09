#кнопка уведомлений бота о истечении его подписки


import discord
from discord import ui
from config.settings import SUBSCRIPTION_CHANNEL_ID
from datetime import datetime
from utils.storage import add_application, add_application_sub
from utils.logger import send_log


class SubscriptionModal(discord.ui.Modal, title='Информация о подписке'):
    """Кнопка для заполнения даты"""

    date_input = discord.ui.TextInput(
        label='Введи ДД.ММ.ГГГГ',
        placeholder='например 04.03.2026',
        min_length=10,
        max_length=10
    )

    async def on_submit(self, interaction: discord.Interaction):
        raw_date = self.date_input.value

        try:
            # Парсим дату для проверки корректности
            day, month, year = map(int, raw_date.split('.'))

            # 2. Получаем канал через get_channel (из контекста сервера)
            channel = interaction.guild.get_channel(SUBSCRIPTION_CHANNEL_ID)

            # Подготовка данных для JSON
            app_data = {
                'user_id': interaction.user.id,
                'user_name': str(interaction.user),
                'day': day,
                'month': month,
                'year': year,
                'timestamp': datetime.utcnow().isoformat()
            }

            add_application_sub(app_data)

            # Создание Embed
            embed = discord.Embed(
                title='Информация обновлена',
                description=f'Новая дата истечения: **{raw_date}**',
                color=discord.Color.gold(),
                timestamp=datetime.utcnow()
            )

            # Отправка лога и ответа
            await interaction.response.send_message("✅ Данные успешно сохранены!", ephemeral=True)

            if channel:
                await channel.send(embed=embed)

            await send_log(
                interaction.guild,
                f'📋 **Время подписки обновлено**\nПользователь: {interaction.user.mention}',
                discord.Color.gold()
            )

        except ValueError:
            await interaction.response.send_message("❌ Неверный формат даты! Используйте ДД.ММ.ГГГГ", ephemeral=True)


# 2. Кнопка, которая вызывает это модальное окно
class SubscriptionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @ui.button(label="Информация о подписке", style=discord.ButtonStyle.primary, custom_id="create_notification_btn")
    async def notification_button(self, interaction: discord.Interaction, button: ui.Button):
        # Вызываем модальное окно при нажатии
        await interaction.response.send_modal(SubscriptionModal())

