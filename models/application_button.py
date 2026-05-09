"""Кнопка для открытия модального окна заявки"""
import discord
from models.application_modal import FamilyApplicationModal, AFKApplicationReviewView
from utils.role_manager import remove_applicant_role
from config.settings import CAPTS_FILE
from utils.storage import load_capt_participants, save_capt_participants



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
        subject = "на AFK" if self.is_afk else "в семью"

        await interaction.response.send_message(f"❌ Заявка отклонена.", ephemeral=True)
        self.stop()
        await interaction.message.edit(view=None)

        try:
            await self.applicant.send(f"😔 К сожалению, ваша заявка {subject} была отклонена.")
        except:
            pass


class CaptPanelButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Вечные кнопки

    @discord.ui.button(label="Принять", style=discord.ButtonStyle.green, custom_id="capt_accept_unique_id")
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Работаем через ID пользователя (int), так как это надежнее всего для JSON
        user_id = interaction.user.id

        # Читаем актуальный список из JSON-файла заявок
        participants = load_capt_participants()

        # Проверяем, записан ли уже игрок
        if user_id in participants:
            await interaction.response.send_message("❌ Вы уже записаны на капт!", ephemeral=True)
            return

        # Добавляем ID игрока в список и сохраняем файл
        participants.append(user_id)
        save_capt_participants(participants)

        # Строим текстовые пинги в столбик <@ID>
        participants_text = "\n".join([f"{idx + 1}. <@{uid}>" for idx, uid in enumerate(participants)])

        # Получаем текущий Embed из сообщения и обновляем его описание
        embed = interaction.message.embeds[0]
        embed.description = (
            "НАЖМИТЕ НА ПРИНЯТЬ, ЕСЛИ ВЫ ХОТИТЕ УЧАСТВОВАТЬ В КАПТЕ\n"
            "НАЖМИТЕ НА УДАЛИТЬ, ЕСЛИ ХОТИТЕ, ЧТОБЫ ВСЕ УЧАСТНИКИ УДАЛИЛИСЬ\n\n"
            f"**СПИСОК УЧАСТНИКОВ ({len(participants)}):**\n{participants_text}"
        )

        # Редактируем сообщение (обновляем эмбед прямо в Дискорде)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Удалить участников", style=discord.ButtonStyle.red, custom_id="capt_clear_unique_id")
    async def clear_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Проверка прав администратора
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ У вас нет прав для очистки списка!", ephemeral=True)
            return

        # Полностью очищаем список в JSON-файле заявок
        save_capt_participants([])

        # Возвращаем Embed к исходному состоянию без списка
        embed = interaction.message.embeds[0]
        embed.description = (
            "НАЖМИТЕ НА ПРИНЯТЬ, ЕСЛИ ВЫ ХОТИТЕ УЧАСТВОВАТЬ В КАПТЕ\n"
            "НАЖМИТЕ НА УДАЛИТЬ, ЕСЛИ ХОТИТЕ, ЧТОБЫ ВСЕ УЧАСТНИКИ УДАЛИЛИСЬ\n\n"
            "**СПИСОК УЧАСТНИКОВ (0):**\n*Список пуст*"
        )

        # Обновляем сообщение
        await interaction.response.edit_message(embed=embed)
