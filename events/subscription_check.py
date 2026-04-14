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
        await self.bot.wait_until_ready()

        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                subs = json.load(f)
            except:
                return

        channel = self.bot.get_channel(SUBSCRIPTION_CHANNEL_ID)
        if not channel: return

        today = date.today()

        for sub in subs:
            try:
                end_date = date(sub['year'], sub['month'], sub['day'])
                delta = (end_date - today).days

                # подписка истекла
                if delta < 0:
                    def is_bot(m): return m.author == self.bot.user

                    await channel.purge(limit=10, check=is_bot)
                    print(f"🧹 Старые уведомления для {sub['user_name']} удалены, так как срок вышел.")
                    continue

                # подписка скоро закончится
                if 0 <= delta <= 3:
                    # Сначала удаляем старое сообщение бота, чтобы не спамить
                    await channel.purge(limit=5, check=lambda m: m.author == self.bot.user and "Внимание" in m.content)

                    if delta > 0:
                        await channel.send(
                            f"⚠️ **Внимание!**\nПодписка <@{sub['user_id']}> истекает через **{delta}** дн.\n"
                            f"Дата окончания: `{end_date.strftime('%d.%m.%Y')}`"
                        )
                    else:
                        await channel.send(f"🚨 **Срочно!** Подписка <@{sub['user_id']}> истекает **сегодня**!")

            except Exception as e:
                print(f"Ошибка: {e}")



# функция регистрации
async def setup_subscription_task(bot):
    if not bot.get_cog("SubscriptionTasks"):
        await bot.add_cog(SubscriptionTasks(bot))
