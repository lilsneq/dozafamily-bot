"""Кнопка для открытия модального окна заявки"""
import discord
from models.application_modal import FamilyApplicationModal


class ApplicationButton(discord.ui.View):
    """Кнопка для открытия модального окна заявки"""
    
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label='📝 Подать заявку в семью',
        style=discord.ButtonStyle.primary,
        custom_id='family_application_button'
    )
    async def application_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FamilyApplicationModal())



class ApplicationReviewView(discord.ui.View):
    """Кнопки под заявкой в админ-канале"""

    def __init__(self, applicant: discord.Member, app_id: int):
        super().__init__(timeout=None)
        self.applicant = applicant
        self.app_id = app_id

    @discord.ui.button(label="Принять", style=discord.ButtonStyle.green, custom_id="approve_btn")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Логика принятия
        from utils.role_manager import give_accepted_roles

        success = await give_accepted_roles(self.applicant)
        if success:
            await interaction.response.send_message(f"✅ Заявка #{self.app_id} одобрена. Роли выданы.", ephemeral=True)
            # Отключаем кнопки после нажатия
            self.stop()
            await interaction.message.edit(view=None)
            #ЛС пользователю
            await self.applicant.send(f"🎉 Ваша заявка #{self.app_id} в семью была одобрена!")
        else:
            await interaction.response.send_message("❌ Ошибка при выдаче ролей. Проверьте права бота.", ephemeral=True)

    @discord.ui.button(label="Отклонить", style=discord.ButtonStyle.red, custom_id="deny_btn")
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Логика отклонения
        await interaction.response.send_message(f"❌ Заявка #{self.app_id} отклонена.", ephemeral=True)
        self.stop()
        await interaction.message.edit(view=None)
        await self.applicant.send(f"😔 К сожалению, ваша заявка #{self.app_id} в семью была отклонена.")
