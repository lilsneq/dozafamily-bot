import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from config.settings import APPLICATIONS_FILE


def load_applications_data():
    """Загрузка данных из applications.json"""
    try:
        if os.path.exists(APPLICATIONS_FILE):
            with open(APPLICATIONS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('applications', {})
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
    return {}

def get_user_static(user_id):
    """Получить статик пользователя по его ID"""
    applications = load_applications_data()
    for app in applications.values():
        if app.get('user_id') == user_id:
            return app.get('passport')
    return None

def setup_static_commands(bot):
    """Настройка команд для статика"""

    @bot.tree.command(name='static', description='Показать статик пользователя')
    @app_commands.describe(user='Пользователь, чей статик показать')
    async def static_command(interaction: discord.Interaction, user: discord.Member):
        """Команда для показа статика пользователя"""
        static = get_user_static(user.id)

        if static:
            embed = discord.Embed(
                title=f'📋 Статик пользователя {user.name}',
                description=f'**Пользователь:** {user.mention}\n**Статик:** {static}',
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=user.display_avatar.url)
        else:
            embed = discord.Embed(
                title='❌ Статик не найден',
                description=f'У пользователя {user.mention} нет сохраненного статика.',
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

