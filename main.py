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
        try:
            await self.add_cog(SubscriptionTasks(self))
            print("Задача проверки подписок запущена")
        except Exception as e:
            print(f'Ошибка проверки подписок {e}')

            self.tree.add_command(new_capt_command)

            setup_static_commands(self)
            setup_bot_events(self)
            setup_server_events(self)

            print("✅ Все команды и события зарегистрированы")

def main():
    if not TOKEN:
        print('❌ Ошибка: TOKEN не найден!')
        return

    bot = MyBot()


    print('🚀 Запуск бота...')
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
