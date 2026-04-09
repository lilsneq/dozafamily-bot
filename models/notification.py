#кнопка уведомлений бота о истечении его подписки


import discord
from discord import ui
from config.settings import SUBSCRIPTION_CHANNEL_ID
from datetime import datetime
from utils.storage import add_application, add_application_sub
from utils.logger import send_log
from datetime import datetime, timedelta


class SubscriptionModal(discord.ui.Modal, title='Информация о подписке'):
    """Кнопка для заполнения даты"""

    date_input = discord.ui.TextInput(
        label='Введи дату начала подписки ДД.ММ.ГГГГ',
        placeholder='например 04.03.2026',
        min_length=10,
        max_length=10
    )




    async def on_submit(self, interaction: discord.Interaction):
        raw_date = self.date_input.value

        try:
            # Парсим введенную дату (дату начала)
            start_date = datetime.strptime(raw_date, "%d.%m.%Y")

            # ВЫЧИСЛЯЕМ дату окончания (+30 дней)
            end_date = start_date + timedelta(days=30)

            app_data = {
                'user_id': interaction.user.id,
                'user_name': str(interaction.user),
                'start_date': start_date.strftime("%d.%m.%Y"),
                # Сохраняем компоненты даты окончания для задачи проверки
                'day': end_date.day,
                'month': end_date.month,
                'year': end_date.year,
                'timestamp': datetime.utcnow().isoformat()
            }

            add_application_sub(app_data)

            embed = discord.Embed(
                title='Подписка зарегистрирована',
                description=(
                    f'Дата начала: **{raw_date}**\n'
                    f'Дата окончания: **{end_date.strftime("%d.%m.%Y")}**\n\n'
                    f'Бот напомнит вам об оплате за 3 дня до конца.'
                ),
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )

            await interaction.response.send_message("✅ Данные сохранены! Окончание через 30 дней.", ephemeral=True)

            channel = interaction.guild.get_channel(SUBSCRIPTION_CHANNEL_ID)
            if channel:
                await channel.send(embed=embed)

        except ValueError:
            await interaction.response.send_message("❌ Ошибка! Используйте формат ДД.ММ.ГГГГ (например, 09.04.2026)",
                                                    ephemeral=True)



# 2. Кнопка, которая вызывает это модальное окно
class SubscriptionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @ui.button(label="Информация о подписке", style=discord.ButtonStyle.primary, custom_id="create_notification_btn")
    async def notification_button(self, interaction: discord.Interaction, button: ui.Button):
        # Вызываем модальное окно при нажатии
        await interaction.response.send_modal(SubscriptionModal())

