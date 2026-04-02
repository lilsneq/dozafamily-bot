"""Кнопка для открытия модального окна заявки"""
import discord
from models.application_modal import FamilyApplicationModal, AFKApplicationReviewView


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


class AFKApplicationButton(discord.ui.View):
    """AFK Кнопка для открытия модального окна заявки"""

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label='📝 Подать заявку на афк',
        style=discord.ButtonStyle.primary,
        custom_id='afk_application_button'
    )
    async def afk_application_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AFKApplicationReviewView())


class ApplicationReviewView(discord.ui.View):
    """Кнопки под заявкой в админ-канале (Общие для всех типов)"""

    def __init__(self, applicant: discord.Member, app_id: int, is_afk: bool = False):
        super().__init__(timeout=None)
        self.applicant = applicant
        self.app_id = app_id
        self.is_afk = is_afk  # Флаг: AFK это или обычная заявка

    @discord.ui.button(label="Принять", style=discord.ButtonStyle.green, custom_id="approve_btn")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        from utils.role_manager import give_accepted_roles, give_afk_role

        # Выбираем, какую функцию выдачи ролей вызвать
        if self.is_afk:
            success = await give_afk_role(self.applicant)
            msg_text = f"✅ AFK-заявка #{self.app_id} одобрена. Роль AFK выдана."
            dm_text = f"🎉 Ваш запрос на AFK #{self.app_id} был одобрен!"
        else:
            success = await give_accepted_roles(self.applicant)
            msg_text = f"✅ Заявка #{self.app_id} одобрена. Роли семьи выданы."
            dm_text = f"🎉 Ваша заявка #{self.app_id} в семью была одобрена!"

        if success:
            await interaction.response.send_message(msg_text, ephemeral=True)
            self.stop()
            await interaction.message.edit(view=None)
            try:
                await self.applicant.send(dm_text)
            except:
                pass
        else:
            await interaction.response.send_message("❌ Ошибка при выдаче ролей. Проверьте права бота.", ephemeral=True)

    @discord.ui.button(label="Отклонить", style=discord.ButtonStyle.red, custom_id="deny_btn")
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        subject = "на AFK" if self.is_afk else "в семью"

        await interaction.response.send_message(f"❌ Заявка #{self.app_id} отклонена.", ephemeral=True)
        self.stop()
        await interaction.message.edit(view=None)

        try:
            await self.applicant.send(f"😔 К сожалению, ваша заявка #{self.app_id} {subject} была отклонена.")
        except:
            pass
