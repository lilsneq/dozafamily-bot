"""Команды для работы с заявками"""
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from utils.storage import get_application, update_application
from utils.logger import send_log
from models.application_button import ApplicationButton
from utils.role_manager import give_accepted_roles, remove_applicant_role


def setup_application_commands(bot):
    """Настройка команд для работы с заявками"""

    @bot.command(name='accept')
    @commands.has_permissions(manage_guild=True)
    async def accept_application(ctx, app_id: int):
        """Принять заявку"""
        app = get_application(app_id)

        if not app:
            await ctx.send(f'❌ Заявка #{app_id} не найдена!')
            return

        if app['status'] != 'pending':
            await ctx.send(f'❌ Заявка #{app_id} уже обработана (статус: {app["status"]})!')
            return

        # Обновление статуса
        update_application(app_id, {
            'status': 'accepted',
            'processed_by': ctx.author.id,
            'processed_at': datetime.utcnow().isoformat()
        })

        # Отправка уведомления пользователю
        try:
            user = await bot.fetch_user(app['user_id'])
            embed = discord.Embed(
                title='✅ Заявка принята!',
                description=f'Ваша заявка #{app_id} в семью была принята! Пожалуйста сделайте ник по форме ниже:\n\n`Имя Фамилия | OOC Имя`',
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Принял', value=f'{ctx.author.mention} ({ctx.author.name})', inline=False)
            embed.add_field(name='Имя и Фамилия', value=app['full_name'], inline=False)

            await user.send(embed=embed)
        except Exception as e:
            await ctx.send(f'⚠️ Не удалось отправить уведомление пользователю: {e}')

        # Ответ в канал
        await ctx.send(f'✅ Заявка #{app_id} от пользователя <@{app["user_id"]}> принята!')

        # Выдача ролей принятого и снятие роли заявителя
        try:
            member = ctx.guild.get_member(app['user_id'])
            if member:
                await give_accepted_roles(member)
                await remove_applicant_role(member)
        except Exception as e:
            print(f"Ошибка при выдаче ролей: {e}")

        # Лог
        await send_log(
            ctx.guild,
            f'✅ **Заявка принята #{app_id}**\nПринял: {ctx.author.mention}\nПодавал: <@{app["user_id"]}>\nИмя: {app["full_name"]}\nВыданы роли принятого и снята роль заявителя',
            discord.Color.green()
        )

    @bot.command(name='decline')
    @commands.has_permissions(manage_guild=True)
    async def decline_application(ctx, app_id: int, *, reason: str):
        """Отклонить заявку"""
        app = get_application(app_id)

        if not app:
            await ctx.send(f'❌ Заявка #{app_id} не найдена!')
            return

        if app['status'] != 'pending':
            await ctx.send(f'❌ Заявка #{app_id} уже обработана (статус: {app["status"]})!')
            return

        # Обновление статуса
        update_application(app_id, {
            'status': 'declined',
            'processed_by': ctx.author.id,
            'decline_reason': reason,
            'processed_at': datetime.utcnow().isoformat()
        })

        # Отправка уведомления пользователю
        try:
            user = await bot.fetch_user(app['user_id'])
            embed = discord.Embed(
                title='❌ Заявка отклонена',
                description=f'Ваша заявка #{app_id} в семью была отклонена.',
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Отклонил', value=f'{ctx.author.mention} ({ctx.author.name})', inline=False)
            embed.add_field(name='Причина', value=reason, inline=False)
            embed.add_field(name='Имя и Фамилия', value=app['full_name'], inline=False)

            await user.send(embed=embed)
        except Exception as e:
            await ctx.send(f'⚠️ Не удалось отправить уведомление пользователю: {e}')

        # Ответ в канал
        await ctx.send(f'❌ Заявка #{app_id} от пользователя <@{app["user_id"]}> отклонена.\nПричина: {reason}')

        # Лог
        await send_log(
            ctx.guild,
            f'❌ **Заявка отклонена #{app_id}**\nОтклонил: {ctx.author.mention}\nПодавал: <@{app["user_id"]}>\nИмя: {app["full_name"]}\nПричина: {reason}',
            discord.Color.red()
        )

    # Обработка ошибок команд
    @accept_application.error
    async def accept_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('❌ У вас нет прав для выполнения этой команды!')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('❌ Использование: `l.accept <номер заявки>`')
        else:
            await ctx.send(f'❌ Произошла ошибка: {error}')

    @decline_application.error
    async def decline_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('❌ У вас нет прав для выполнения этой команды!')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('❌ Использование: `l.decline <номер заявки> <причина>`')
        else:
            await ctx.send(f'❌ Произошла ошибка: {error}')