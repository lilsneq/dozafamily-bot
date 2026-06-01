# МОДАЛЬНОЕ ОКНО ДЛЯ ЗАЯВКИ НА ПОВЫШЕНИЕ
import logging

# ИМПОРТЫ

import discord
from discord.app_commands import guilds

from config.settings import RATING_CHANNEL_ID, ADMIN_RATING_CHANNEL_ID



# СКРИПТ


class RatingDrop(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Recruit", value="1482962712844828713:1", description="Подать заявку Recruit", emoji="🔵"),
            discord.SelectOption(label="Sora", value="1482962888762069192:2", description="Подать заявку Sora", emoji="⚫"),
            discord.SelectOption(label="Main Sora", value="1508432058865684671:3", description="Подать заявку Main Sora", emoji="🔴"),
            # discord.SelectOption(label="Chif rec", value="1509926246505779270:4", description="Подать заявку Chif rec", emoji="🟢"),
            # discord.SelectOption(label="High", value="1487937197142179880:5", description="Подать заявку High", emoji="🔵"),
            # discord.SelectOption(label="Dep", value="1487937119853744358:6", description="Подать заявку Dep", emoji="🔴"),
        ]

        super().__init__(
            placeholder="Выберите желаемый номер для повышения...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="rating_system_dropdown"
        )

    async def callback(self, interaction: discord.Interaction):
        role_id_str, number = self.values[0].split(":")
        role_id = int(role_id_str)

        await self.view.assign_role(interaction, role_id=role_id, number=number)


class RatingSystemApplication(discord.ui.View):
    """ОКНО НА ПОВЫШЕНИЕ"""
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RatingDrop())

    async def assign_role(self, interaction: discord.Interaction, role_id: int, number: str):
        guild = interaction.guild
        role = guild.get_role(role_id)

        if not role:
            await interaction.response.send_message(
                f'Ошибка: Роль не найдена на сервере',
                ephemeral=True,
            )
            return

        if role in interaction.user.roles:
            await interaction.response.send_message(
                f'У вас уже есть роль {role.name}',
                ephemeral=True,
            )
            return

        admin_ch = guild.get_channel(ADMIN_RATING_CHANNEL_ID)
        if admin_ch:
            admin_embed = discord.Embed(
                title='Заявка на повышение',
                color=discord.Color.green()
            )
            admin_embed.add_field(name="Пользователь", value=interaction.user.mention, inline=True)
            admin_embed.add_field(name="Запрашиваемая роль", value=role.mention, inline=False)
            admin_embed.set_footer(text=f"User ID: {interaction.user.id}")

            await admin_ch.send(embed=admin_embed, view=AdminAcceptRatingSystem())

            await interaction.response.send_message(
                f'Ваша заявка успешно отправлена',
                ephemeral=True,
            )

        else:
            logging.error('Канал рассмотрения заявок не найдена')
            return


class AdminAcceptRatingSystem(discord.ui.View):
    """ПАНЕЛЬ ОДОБРИТЬ/ОТКЛОНИТЬ У АДМИНА"""
    def __init__(self):
        super().__init__(timeout=None)

        self.all_rating_roles = [
            1482962712844828713,
            1482962888762069192,
            1508432058865684671,
            1509926246505779270,
            1487937197142179880,
            1487937119853744358
        ]


    @discord.ui.button(label='Одобрить', style=discord.ButtonStyle.green, custom_id="admin_aprove")
    async def button_admin_aprove(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild

        if not interaction.message.embeds:
            await interaction.response.send_message("Пользователь или роль не найдены на сервере.", ephemeral=True)
            return
        embed = interaction.message.embeds[0]

        try:
            footer_text = embed.footer.text
            parts = footer_text.split("|")

            user_part = parts[0].split(":")
            user_id = int(user_part[1].strip())

            role_part = parts[1].split(":")
            role_id = int(role_part[1].strip())

        except Exception:
            logging.error(f"Не удалось распарсить эмбед")
            await interaction.response.send_message(
                "Не удалось автоматически считать ID пользователя или роли из этой карточки.", ephemeral=True)
            return

        member = guild.get_member(user_id)
        role = guild.get_role(role_id)

        if not member or not role:
            await interaction.response.send_message(" Пользователь или роль больше не найдены на сервере.", ephemeral=True)
            return

        try:
            roles_to_remove = []
            for r_id in self.all_rating_roles:
                old_role = guild.get_role(r_id)
                if old_role and old_role in member.roles and r_id != role_id:
                    roles_to_remove.append(old_role)

            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)
                logging.info(f"Удалены старые роли номеров ({len(roles_to_remove)} шт.) у пользователя {member.name}")

            await member.add_roles(role)

            embed.color = discord.Color.brand_green()
            embed.title = f"Заявка одобрена администратором {interaction.user.display_name}"

            await interaction.message.edit(embed=embed, view=None)
            await interaction.response.defer()

        except Exception:
            logging.error('Ошибка одобрения роли')


    @discord.ui.button(label="Отклонить", style=discord.ButtonStyle.red, custom_id="admin_deny")
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.message.embeds:
            return
        embed = interaction.message.embeds[0]

        try:
            footer_text = embed.footer.text
            parts = footer_text.split("|")

            user_part = parts[0].split(":")
            user_id = int(user_part[1].strip())

            member = interaction.guild.get_member(user_id)
        except Exception as e:
            logging.error(f'ОШИБКА КНОПКИ ОТКЛОНИТЬ: {e}')
            member = None

        embed.color = discord.Color.red()
        embed.title = f"Заявка отклонена администратором {interaction.user.display_name}"

        await interaction.message.edit(embed=embed, view=None)
        await interaction.response.defer()
        if member:
            logging.info(f"Администратор {interaction.user.name} отклонил заявку пользователя {member.name}")





