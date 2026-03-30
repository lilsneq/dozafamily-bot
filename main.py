"""
Discord Bot для системы заявок в семью
Модульная структура проекта
"""
import discord
from discord.ext import commands

from config.settings import TOKEN
from commands.application_commands import setup_application_commands
from commands.static import setup_static_commands
from events.bot_events import setup_bot_events
from events.server_events import setup_server_events
import ssl
import os



# Этот блок исправляет ошибку сертификатов на macOS
if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context




def main():
    """Главная функция запуска бота"""
    
    # Проверка токена
    if not TOKEN:
        print('❌ Ошибка: DISCORD_TOKEN не найден в .env файле!')
        return
    
    # Intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    
    # Создание бота
    bot = commands.Bot(command_prefix='l.', intents=intents, status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name='majestic-rp.ru'), help_command=None)
    
    # Настройка команд
    setup_application_commands(bot)
    setup_static_commands(bot)

    # Настройка событий
    setup_bot_events(bot)
    setup_server_events(bot)
    
    # Запуск бота
    print('🚀 Запуск бота...')
    bot.run(TOKEN)


if __name__ == '__main__':
    main()