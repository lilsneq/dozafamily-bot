"""События бота"""
import asyncio

from config.settings import PANEL_CHANNEL_ID, RULES_CHANNEL_ID, AFK_CHANNEL_ID, SUBSCRIPTION_CHANNEL_ID, CAPT_CHANNEL_ID
from models.application_button import ApplicationButton, AFKApplicationButton
from models.rules_button import RulesButton
from utils.storage import load_applications
from utils.logger import send_log
import discord
from models.capt_button import CaptApplicationButton
from models.notification import SubscriptionModal, SubscriptionView


def setup_bot_events(bot):
    """Настройка событий бота"""

    @bot.event
    async def on_ready():
        """Событие при запуске бота"""
        load_applications()
        print(f'Бот запущен как {bot.user}')

        # Синхронизация команд
        try:
            synced = await bot.tree.sync()
            print(f'Синхронизировано {len(synced)} команд')
        except Exception as e:
            print(f'Ошибка синхронизации команд: {e}')

        # Автоматическая очистка канала панели и создание новой панели
        for guild in bot.guilds:
            try:
                panel_channel = guild.get_channel(PANEL_CHANNEL_ID)
                if panel_channel:
                    # Удаление всех сообщений в канале
                    deleted = 0
                    async for message in panel_channel.history(limit=None):
                        try:
                            await message.delete()
                            deleted += 1
                        except Exception as e:
                            print(f'Не удалось удалить сообщение: {e}')

                    print(f'Удалено {deleted} сообщений из канала панели')

                    # Создание новой панели заявок
                    family_embed = discord.Embed(
                        title='🏠 Заявка в семью',
                        description='Нажмите на кнопку ниже, чтобы подать заявку на вступление в семью.\n\n'
                                    '**Требования:**\n'
                                    '• Заполните все поля честно\n'
                                    '• Укажите реальную информацию\n'
                                    '• Дождитесь рассмотрения заявки',
                        color=discord.Color.blue()
                    )

                    #фотки у сообщения
                    file = discord.File("assets/rules.jpg", filename="rules.jpg")
                    family_embed.set_image(url="attachment://rules.jpg")
                    family_embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

                    view = ApplicationButton()

                    await panel_channel.send(file=file, embed=family_embed, view=view)

                    print(f'Панель заявок создана в канале {panel_channel.name}')

                    # Лог о создании панели
                    await send_log(
                        guild,
                        f'🔧 **Панель заявок автоматически создана**\nМодератор: Автоматически\nКанал: {panel_channel.mention}',
                        discord.Color.blue()
                    )
            except Exception as e:
                print(f'Ошибка при работе с каналом панели: {e}')

        #afk эмбед и очиска канала
        for g in bot.guilds:
            try:
                afk_channel = g.get_channel(AFK_CHANNEL_ID)
                if afk_channel:
                    # Удаление всех сообщений в канале
                    deleted = 0
                    async for message in afk_channel.history(limit=None):
                        try:
                            await message.delete()
                            deleted += 1
                        except Exception as e:
                            print(f'Не удалось удалить сообщение: {e}')

                    print(f'Удалено {deleted} сообщений из канала AFK')

                    # Создание новой панели заявок
                    afk_embed = discord.Embed(
                        title='🏠 Inactive',
                        description='Нажмите на кнопку ниже, чтобы подать заявку на inactive.',
                        color=discord.Color.blue()
                    )

                    file = discord.File("assets/rules.jpg", filename="rules.jpg")

                    afk_embed.set_image(url="attachment://rules.jpg")
                    afk_embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

                    view = AFKApplicationButton()

                    await afk_channel.send(file=file, embed=afk_embed, view=view)
                    print(f'Панель AFK создана в канале {afk_channel.name}')

                    # Лог о создании панели
                    await send_log(
                        guild,
                        f'🔧 **Панель AFK автоматически создана**\nМодератор: Автоматически\nКанал: {afk_channel.mention}',
                        discord.Color.blue()
                    )
            except Exception as e:
                print(f'Ошибка при работе с каналом панели: {e}')


            # Отправка эмбеда с правилами
            try:
                print('Панель правил запущен')
                rules_channel = guild.get_channel(RULES_CHANNEL_ID)
                if rules_channel:
                    await rules_channel.purge()

                    from models.rules_button import RulesButton
                    await RulesButton.send_rules(rules_channel)

                    print(f'Эмбед с правилами (локальное фото) отправлен в {rules_channel.name}')
            except Exception as e:
                print(f'Ошибка при отправке правил: {e}')


        #ЧАТ ПОДПИСКИ БОТА
        sub_channel = bot.get_channel(SUBSCRIPTION_CHANNEL_ID)
        if sub_channel:
            await sub_channel.purge(check=lambda m: m.author == bot.user)

            emb = discord.Embed(title='Кнопка подписки', color=discord.Color.red())
            file = discord.File("assets/rules.jpg", filename="rules.jpg")
            emb.set_image(url="attachment://rules.jpg")

            await sub_channel.send(file=file, embed=emb, view=SubscriptionView())
            bot.add_view(SubscriptionView())
            print(f'Панель пописки создана{sub_channel.name}')


        #ЧАТ КАПТОВ
        capt_channel = bot.get_channel(CAPT_CHANNEL_ID)
        if capt_channel:
            await capt_channel.purge(check=lambda m: m.author == bot.user)

            emb = discord.Embed(title=' Создание чата для откатов', color=discord.Color.red())
            file = discord.File("assets/rules.jpg", filename="rules.jpg")
            emb.set_image(url="attachment://rules.jpg")

            await capt_channel.send(file=file, embed=emb, view=CaptApplicationButton())
            bot.add_view(CaptApplicationButton())
            print(f'Панель откатов создана в {capt_channel.name}')


        # Логирование запуска
        for guild in bot.guilds:
            await send_log(
                guild,
                f'✅ **Бот запущен**\nБот {bot.user.mention} успешно запущен и готов к работе!',
                discord.Color.green()
            )


