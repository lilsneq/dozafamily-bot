"""Кнопка для открытия модального окна заявки"""
import discord
import re
from models.application_modal import FamilyApplicationModal, AFKApplicationReviewView
from utils.role_manager import remove_applicant_role
from config.settings import CAPTS_FILE
from utils.storage import (
    load_capt_participants,
    save_capt_participants,
    load_capt_data,
    save_capt_data,
    is_capt_locked,
    set_capt_lock
)
from config.settings import DEP_ROLE_ID, HIGH_ROLE_ID, RECRUIT_ROLE_ID

# ИСПРАВЛЕНИЕ ИМПОРТА: Добавили функции load_capt_data и save_capt_data, чтобы они не выдавали NameError
from utils.storage import load_capt_participants, save_capt_participants, load_capt_data, save_capt_data





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
    """Кнопки под заявкой в админ-канале"""
    ALLOWED_ROLE = [DEP_ROLE_ID, HIGH_ROLE_ID, RECRUIT_ROLE_ID]

    def __init__(self, applicant: discord.Member, app_id: int, is_afk: bool = False):
        super().__init__(timeout=None)
        self.applicant = applicant
        self.app_id = app_id
        self.is_afk = is_afk  # Флаг: AFK это или обычная заявка



    @discord.ui.button(label="Принять", style=discord.ButtonStyle.green, custom_id="approve_btn")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        from utils.role_manager import give_accepted_roles, give_afk_role

        # кнопка нажимается только если ты админ
        has_allowed_roles = any(role.id in self.ALLOWED_ROLE for role in interaction.user.roles)
        if not (interaction.user.guild_permissions.administrator or has_allowed_roles):
            await interaction.response.send_message("❌ Эта кнопка доступна только администраторам.", ephemeral=True)
            return

        await remove_applicant_role(interaction.user)


        # Выбираем, какую функцию выдачи ролей вызвать
        if self.is_afk:
            success = await give_afk_role(self.applicant)
            msg_text = f"✅ AFK-заявка одобрена. Роль AFK выдана."
            dm_text = f"🎉 Ваш запрос на AFK был одобрен!"
        else:
            success = await give_accepted_roles(self.applicant)
            msg_text = f"✅ Заявка одобрена. Роли семьи выданы."
            dm_text = f"🎉 Ваша заявка в семью была одобрена!"

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
        has_allowed_roles = any(role.id in self.ALLOWED_ROLE for role in interaction.user.roles)
        if not (interaction.user.guild_permissions.administrator or has_allowed_roles):
            await interaction.response.send_message("❌ Эта кнопка доступна только администраторам.", ephemeral=True)
            return

        subject = "на AFK" if self.is_afk else "в семью"

        await interaction.response.send_message(f"❌ Заявка отклонена.", ephemeral=True)
        self.stop()
        await interaction.message.edit(view=None)

        try:
            await self.applicant.send(f" К сожалению, ваша заявка {subject} была отклонена.")
        except:
            pass


class CaptPanelButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Вечные кнопки

    @discord.ui.button(label="Принять", style=discord.ButtonStyle.green, custom_id="capt_accept_unique_id")
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        embed = interaction.message.embeds[0]
        match = re.search(r'№(\d+)', embed.title)
        if match:
            capt_id = match.group(1)
        else:
            await interaction.followup.send("❌ Не удалось определить номер капта.", ephemeral=True)
            return

        if is_capt_locked(capt_id):
            await interaction.followup.send(f"🔒 Запись на Капт №{capt_id} уже закрыта администрацией!", ephemeral=True)
            return

        participants = load_capt_participants()

        if interaction.user.id in participants:
            await interaction.followup.send(f"❌ Вы уже записаны на Капт №{capt_id}!", ephemeral=True)
            return

        participants.append(interaction.user.id)
        save_capt_participants(participants)

        participants_text = "\n".join([f"{idx + 1}. <@{uid}>" for idx, uid in enumerate(participants)])

        embed.description = (
            "НАЖМИТЕ НА ПРИНЯТЬ, ЕСЛИ ВЫ ХОТИТЕ УЧАСТВОВАТЬ В КАПТЕ\n"
            "НАЖМИТЕ НА УДАЛИТЬ, ЕСЛИ ХОТИТЕ, ЧТОБЫ ВСЕ УЧАСТНИКИ УДАЛИЛИСЬ\n\n"
            f"**СПИСОК УЧАСТНИКОВ ({len(participants)}):**\n{participants_text}"
        )

        await interaction.message.edit(embeds=[embed])

    @discord.ui.button(label="Удалить участников", style=discord.ButtonStyle.red, custom_id="capt_clear_unique_id")
    async def clear_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ У вас нет прав!", ephemeral=True)
            return

        await interaction.response.defer()
        embed = interaction.message.embeds[0]
        match = re.search(r'№(\d+)', embed.title)
        if not match:
            await interaction.followup.send("❌ Ошибка определения номера панели.", ephemeral=True)
            return

        capt_id = match.group(1)

        save_capt_participants([])

        embed.description = (
            "НАЖМИТЕ НА ПРИНЯТЬ, ЕСЛИ ВЫ ХОТИТЕ УЧАСТВОВАТЬ В КАПТЕ\n"
            "НАЖМИТЕ НА УДАЛИТЬ, ЕСЛИ ХОТИТЕ, ЧТОБЫ ВСЕ УЧАСТНИКИ УДАЛИЛИСЬ\n\n"
            "**СПИСОК УЧАСТНИКОВ (0):**\n*Список пуст*"
        )

        await interaction.message.edit(embeds=[embed])


    @discord.ui.button(label="🔒 Закрыть запись", style=discord.ButtonStyle.secondary, custom_id="capt_toggle_lock_id")
    async def toggle_lock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Проверяем права администратора
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ У вас нет прав для изменения статуса регистрации!",
                                                    ephemeral=True)
            return

        await interaction.response.defer()
        embed = interaction.message.embeds[0]
        match = re.search(r'№(\d+)', embed.title)
        if not match:
            await interaction.followup.send("❌ Ошибка определения номера панели.", ephemeral=True)
            return

        capt_id = match.group(1)

        # Меняем статус на противоположный
        currently_locked = is_capt_locked(capt_id)
        new_status = not currently_locked
        set_capt_lock(capt_id, new_status)

        # Изменяем внешний вид кнопки прямо на панели
        if new_status:
            button.label = " Открыть запись"
            button.style = discord.ButtonStyle.primary
            status_msg = f" Запись на Капт №{capt_id} успешно **закрыта** {interaction.user.mention}."
        else:
            button.label = " Закрыть запись"
            button.style = discord.ButtonStyle.secondary
            status_msg = f" Запись на Капт №{capt_id} успешно **открыта** {interaction.user.mention}."

        # Редактируем сообщение, передавая обновленные эмбед и view с измененной кнопкой
        await interaction.message.edit(embeds=[embed], view=self)

        # Отправляем уведомление модератору в скрытом режиме
        await interaction.followup.send(status_msg, ephemeral=True)

