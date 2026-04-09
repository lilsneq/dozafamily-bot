import discord
from discord.ext import tasks, commands
import json
import os
from datetime import datetime, date
from config.settings import SUBSCRIPTION_CHANNEL_ID

DATA_FILE = 'data/sub.json'


class SubscriptionTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_subscriptions.start()

    def cog_unload(self):
        self.check_subscriptions.cancel()

    @tasks.loop(hours=12)
    async def check_subscriptions(self):
        # 1. Ждем, пока бот полностью загрузится
        await self.bot.wait_until_ready()

        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                subs = json.load(f)
            except:
                return

        # 2. Ищем канал (сначала в кэше, потом через fetch)
        channel = self.bot.get_channel(SUBSCRIPTION_CHANNEL_ID)
        if not channel:
            try:
                channel = await self.bot.fetch_channel(SUBSCRIPTION_CHANNEL_ID)
            except:
                print(f"❌ Не удалось найти канал с ID {SUBSCRIPTION_CHANNEL_ID}")
                return

        today = date.today()
        print(f"🔎 Запущена проверка подписок... Найдено записей: {len(subs)}")

        for sub in subs:
            try:
                end_date = date(sub['year'], sub['month'], sub['day'])
                delta = (end_date - today).days

                # Отладочный принт в консоль
                print(f"Проверка {sub['user_name']}: осталось {delta} дней.")

                if 0 < delta <= 3:
                    await channel.send(
                        f"⚠️ **Внимание!**\n"
                        f"Подписка пользователя <@{sub['user_id']}> истекает через **{delta}** дн.\n"
                        f"Дата окончания: `{end_date.strftime('%d.%m.%Y')}`"
                    )
                elif delta == 0:
                    await channel.send(f"🚨 **Срочно!** Подписка <@{sub['user_id']}> истекает **сегодня**!")

            except Exception as e:
                print(f"Ошибка при обработке даты для {sub.get('user_name')}: {e}")


# Исправленная функция регистрации
async def setup_subscription_task(bot):
    if not bot.get_cog("SubscriptionTasks"):
        await bot.add_cog(SubscriptionTasks(bot))
