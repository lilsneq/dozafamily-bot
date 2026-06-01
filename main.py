"""
Discord Bot для системы заявок в семью
Модульная структура проекта
"""
import logging
import discord
import sys
import asyncio

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

logging.getLogger("discord").setLevel(logging.WARNING)

from discord.ext import commands
from config.settings import TOKEN
from commands.static import setup_static_commands
from events.bot_events import setup_bot_events
from events.server_events import setup_server_events
from cogs.cogi import new_capt_command
from events.subscription_check import SubscriptionTasks


# СКРИПТ

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix='l.',
    intents=intents,
    status=discord.Status.idle,
    activity=discord.Activity(type=discord.ActivityType.watching, name='majestic-rp.ru'),
    help_command=None
)


async def main():
    if not TOKEN:
        logging.warning('❌ Ошибка: TOKEN не найден!')
        return

    logging.info('🚀 Запуск бота...')

    try:
        await bot.add_cog(SubscriptionTasks(bot))
        bot.tree.add_command(new_capt_command)
        setup_static_commands(bot)
        setup_bot_events(bot)
        setup_server_events(bot)
        logging.info("✅ Все команды и события зарегистрированы")

    except Exception:
        logging.warning('ОШИБКА ЗАПУСКА БОТА', exc_info=True)
        return

    logging.info("✅ БОТ В РАБОТЕ.")

    async with bot:
        await bot.start(TOKEN)



if __name__ == '__main__':
    asyncio.run(main())
