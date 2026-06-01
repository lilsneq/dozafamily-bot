"""События бота"""
import asyncio
import logging
import discord

from config.settings import (PANEL_CHANNEL_ID, RULES_CHANNEL_ID,
                             AFK_CHANNEL_ID, SUBSCRIPTION_CHANNEL_ID,
                             CAPT_CHANNEL_ID, CHANNEL_FOR_CAPT, RATING_CHANNEL_ID)

from models.application_button import ApplicationButton, AFKApplicationButton, CaptPanelButtons
from models.application_rating_system import RatingSystemApplication
from utils.storage import load_applications, start_new_capt_id
from utils.logger import send_log
from models.capt_button import CaptApplicationButton
from models.notification import SubscriptionView



class BotInit:
    def __init__(self, bot):
        self.bot = bot
        self._initialized = False

    #метод запуска всего
    async def run_all(self):
        """ГЛАВНЫЙ МЕТОД ЗАПУСКА ЧАТОВ"""
        if self._initialized:
            logging.info('БОТ ПЕРЕПОДКЛЮЧИЛСЯ')
            return

        logging.info('ИНИЦИАЛИЗАЦИЯ...')

        await self._sub_channel()
        await self._command_sync()
        await self._family_channel_app()
        await self._afk_channel_app()
        await self._rules_channel_app()
        await self._rollback_channel_app()
        await self._create_capt_channel()
        await self._rating_channel_app()

        self._initialized = True
        logging.info('✅ ВСЕ ПАНЕЛИ И СИСТЕМЫ УСПЕШНО ПРОИНИЦИАЛИЗИРОВАЛИСЬ')

    async def _sub_channel(self):
        """ЧАТ ПОДПИСКИ БОТА, в self передовать bot"""
        try:
            sub_channel = self.bot.get_channel(SUBSCRIPTION_CHANNEL_ID)
            if sub_channel:
                # Удаление всех сообщений в канале
                deleted = 0
                async for message in sub_channel.history(limit=None):
                    try:
                        await message.delete()
                        deleted += 1
                    except Exception:
                        logging.error(f'Не удалось удалить сообщение', exc_info=True)

                logging.info(f'Удалено {deleted} сообщений из канала подписки бота')

            if sub_channel:
                await sub_channel.purge(check=lambda m: m.author == self.bot.user)

                emb = discord.Embed(title='Кнопка подписки', color=discord.Color.red())
                file = discord.File("assets/rules.jpg", filename="rules.jpg")
                emb.set_image(url="attachment://rules.jpg")

                await sub_channel.send(file=file, embed=emb, view=SubscriptionView())
                self.bot.add_view(SubscriptionView())
                logging.info(f'Панель пописки создана в {sub_channel.name}')
        except Exception:
            logging.error('ОШИБКА ЧАТА С ПОДПИСКОЙ', exc_info=True)

    async def _command_sync(self):
        """СКОЛЬКО КОМАНД / БОТА СУЩЕСТВУЕТ, в self передовать bot"""
        try:
            synced = await self.bot.tree.sync()
            logging.info(f'Синхронизировано {len(synced)} команд - {synced}')
        except Exception:
            logging.info('Ошибка синхронизации команд', exc_info=True)

    async def _family_channel_app(self):
        """Автоматическая очистка канала панели и создание новой панели, в self передовать bot"""
        for guild in self.bot.guilds:
            try:
                panel_channel = guild.get_channel(PANEL_CHANNEL_ID)
                if panel_channel:
                    deleted = 0
                    async for message in panel_channel.history(limit=None):
                        try:
                            await message.delete()
                            deleted += 1
                        except Exception as e:
                            logging.error(f'Не удалось удалить сообщение: {e}')

                    logging.info(f'Удалено {deleted} сообщений из канала панели')

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

                    logging.info(f'Панель заявок создана в канале {panel_channel.name}')

                    # Лог о создании панели
                    await send_log(
                        guild,
                        f'🔧 **Панель заявок автоматически создана**\nМодератор: Автоматически\nКанал: {panel_channel.mention}',
                        discord.Color.blue()
                    )
            except Exception:
                logging.error('Ошибка при работе с каналом панели', exc_info=True)

    async def _afk_channel_app(self):
        """ЧАТ ЗАЯВКИ НА АФК, в self передовать bot"""
        for guild in self.bot.guilds:
            try:
                afk_channel = guild.get_channel(AFK_CHANNEL_ID)
                if afk_channel:
                    # Удаление всех сообщений в канале
                    deleted = 0
                    async for message in afk_channel.history(limit=None):
                        try:
                            await message.delete()
                            deleted += 1
                        except Exception as e:
                            logging.error(f'Не удалось удалить сообщение: {e}')

                    logging.info(f'Удалено {deleted} сообщений из канала AFK')

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
                    logging.info(f'Панель AFK создана в канале {afk_channel.name}')

                    # Лог о создании панели
                    await send_log(
                        guild,
                        f'🔧 **Панель AFK автоматически создана**\nМодератор: Автоматически\nКанал: {afk_channel.mention}',
                        discord.Color.blue()
                    )
            except Exception:
                logging.error('Ошибка при работе с каналом панели', exc_info=True)

    async def _rules_channel_app(self):
        """Отправка эмбеда с правилами, в self передовать bot"""
        for guild in self.bot.guilds:
            try:
                rules_channel = self.bot.get_channel(RULES_CHANNEL_ID)
                if rules_channel:
                    # Удаление всех сообщений в канале
                    deleted = 0
                    async for message in rules_channel.history(limit=None):
                        try:
                            await message.delete()
                            deleted += 1
                        except Exception as e:
                            logging.error(f'Не удалось удалить сообщение', exc_info=True)

                    logging.info(f'Удалено {deleted} сообщений из канала правил')

                if rules_channel:
                    await rules_channel.purge()

                    from models.rules_button import RulesButton
                    await RulesButton.send_rules(rules_channel)
                logging.info(f'Панель правил запущена в {rules_channel.name}')

            except Exception:
                logging.error('Ошибка при отправке правил', exc_info=True)

        await send_log(
            guild,
            f'🔧 ** Панель заявок повышения автоматически создана**\nМодератором: Автоматически\nКанал: {rating_role_channel.mention}',
            discord.Color.blue()
        )

    async def _rollback_channel_app(self):
        """ЧАТ ОТКАТОВ, в self передовать bot"""
        for guild in self.bot.guilds:
            try:
                rollback_channel = self.bot.get_channel(CAPT_CHANNEL_ID)
                if rollback_channel:
                    # Удаление всех сообщений в канале
                    deleted = 0
                    async for message in rollback_channel.history(limit=None):
                        try:
                            await message.delete()
                            deleted += 1
                        except Exception:
                            logging.error(f'Не удалось удалить сообщение', exc_info=True)

                    logging.info(f'Удалено {deleted} сообщений из канала создания отката')

                if rollback_channel:
                    await rollback_channel.purge(check=lambda m: m.author == self.bot.user)

                    emb = discord.Embed(title=' Создание чата для откатов', color=discord.Color.red())
                    file = discord.File("assets/rules.jpg", filename="rules.jpg")
                    emb.set_image(url="attachment://rules.jpg")

                    await rollback_channel.send(file=file, embed=emb, view=CaptApplicationButton())
                    self.bot.add_view(CaptApplicationButton())

                    logging.info(f'Панель откатов создана в {rollback_channel.name}')

                    await send_log(
                        guild,
                        f'🔧 **Панель заявок автоматически создана**\nМодератор: Автоматически\nКанал: {rollback_channel.mention}',
                        discord.Color.blue())

            except Exception:
                logging.error('Ошибка при работе с каналом панели', exc_info=True)

    async def _create_capt_channel(self):
        """ПАНЕЛЬ ДЛЯ ПРИНЯТИЯ КАПТА"""
        for guild in self.bot.guilds:
            try:
                capt_panel_channel = guild.get_channel(CHANNEL_FOR_CAPT)
                if capt_panel_channel:
                    # Удаление всех сообщений в канале
                    deleted = 0
                    async for message in capt_panel_channel.history(limit=None):
                        try:
                            await message.delete()
                            deleted += 1
                        except Exception:
                            logging.error(f'Не удалось удалить сообщение', exc_info=True)

                    logging.info(f'Удалено {deleted} сообщений из канала принятия капта')
                new_id = start_new_capt_id()

                capt_embed = discord.Embed(
                    title=f'👳🏿‍♀️ЗАЯВКА НА КАПТ №{new_id}',
                    description='НАЖМИТЕ НА ПРИНЯТЬ ЕСЛИ ВЫ ХОТИТЕ УЧАСТВОВАТЬ В КАПТЕ\n'
                                'НАЖМИТЕ НА УДАЛИТЬ ЕСЛИ ХОТИТЕ ЧТОБЫ ВСЕ УЧАСТНИКИ УДАЛИЛИСЬ\n'
                                '/new_capt создание новой панели',
                    color=discord.Color.red()
                )

                view = CaptPanelButtons()

                await capt_panel_channel.send(embed=capt_embed, view=view)

                logging.info(f'Панель заявок на КАПТ создана в канале {capt_panel_channel.name}')

                # Лог о создании панели
                await send_log(
                    guild,
                    f'🔧 **Панель заявок автоматически создана**\nМодератор: Автоматически\nКанал: {capt_panel_channel.mention}',
                    discord.Color.blue()
                )

            except Exception:
                logging.error('Ошибка при работе с каналом панели', exc_info=True)

    async def _rating_channel_app(self):
        for guild in self.bot.guilds:
            try:
                rating_role_channel = guild.get_channel(RATING_CHANNEL_ID)
                if rating_role_channel:
                    # Удаление всех сообщений в канале
                    deleted = 0
                    async for message in rating_role_channel.history(limit=None):
                        try:
                            await message.delete()
                            deleted += 1
                        except Exception as e:
                            logging.error(f'Не удалось удалить сообщение: {e}')

                    logging.info(f'Удалено {deleted} сообщений из канала выдачи ролей')


                rating_embed = discord.Embed(
                    title=f'💣ЗАЯВКА НА ПОВЫШЕНИЕ',
                    description='ВЫБЕРИТЕ РОЛЬ ДЛЯ ПОВЫШЕНИЯ.\n'
                                'ВАША ЗАЯВКА БУДЕТ РАССМОТРЕНА И ПРИНЯТА АДМИНИСТРАЦИЕЙ.',
                    color=discord.Color.pink()
                )

                view = RatingSystemApplication()

                await rating_role_channel.send(embed=rating_embed, view=view)
                logging.info(f'ПАНЕЛЬ ЗАЯВОК НА КАПТ СОЗДАНА В КАНАЛЕ {rating_role_channel.name}')

                await send_log(
                    guild,
                    f'🔧 ** Панель заявок повышения автоматически создана**\nМодератором: Автоматически\nКанал: {rating_role_channel.mention}',
                    discord.Color.blue()
                )

            except Exception:
                logging.error(f'Ошибка при работе с каналом панели', exc_info=True)


def setup_bot_events(bot):
    """Настройка событий бота"""
    initializer = BotInit(bot)

    @bot.event
    async def on_ready():
        """Событие при запуске бота"""
        load_applications()
        logging.info(f'Бот запущен как {bot.user}')

        await initializer.run_all()

        # Логирование запуска
        for guild in bot.guilds:
            await send_log(
                guild,
                f'✅ **Бот запущен**\nБот {bot.user.mention} успешно запущен и готов к работе!',
                discord.Color.green()
            )

























