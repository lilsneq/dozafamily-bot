"""
Discord Bot для системы заявок в семью
Модульная структура проекта
"""

import discord
from discord.ext import commands
from config.settings import TOKEN
from commands.static import setup_static_commands
from events.bot_events import setup_bot_events
from events.server_events import setup_server_events
from cogs.cogi import new_capt_command
from events.subscription_check import SubscriptionTasks
import ssl
import os

# Исправление сертификатов
if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        super().__init__(
            command_prefix='l.',
            intents=intents,
            status=discord.Status.idle,
            activity=discord.Activity(type=discord.ActivityType.watching, name='majestic-rp.ru'),
            help_command=None
        )

    async def setup_hook(self):
        """Этот метод вызывается ПЕРЕД запуском бота (внутри run)"""
        # Регистрируем задачу проверки подписок
        await self.add_cog(SubscriptionTasks(self))
        print("✅ Задача проверки подписок запущена")


def main():
    if not TOKEN:
        print('❌ Ошибка: TOKEN не найден!')
        return

    bot = MyBot()

    bot.tree.add_command(new_capt_command)


    # Настройка команд и событий
    setup_static_commands(bot)
    setup_bot_events(bot)
    setup_server_events(bot)


    print('🚀 Запуск бота...')
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
