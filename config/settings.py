"""Настройки бота"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Токен бота
TOKEN = os.getenv('DISCORD_TOKEN')

# ID каналов
APPLICATION_CHANNEL_ID = 1236151374161641493  # Канал для заявок
LOG_CHANNEL_ID = 1471970109793767544          # Канал для логов
PANEL_CHANNEL_ID = 1488255339819176147        # Канал для панели заявок
STATIC_CHANNEL_ID = 1448565203875926128
RULES_CHANNEL_ID = 1488255736923426938        # Канал для правил
AFK_CHANNEL_ID = 1487901448254521455          # Канал для афк и запросы почему афк
AFK_PANEL_CHANNEL_ID = 1483280022277197865    # Канал для рассмотрения заявок на афк


# ID ролей
APPLICANT_ROLE_ID = 1236152852054016042       # Роль для подающих заявки NO name
ACCEPTED_ROLE_1_ID = 1236152539968438312      # Первая роль принятых Академ
ACCEPTED_ROLE_2_ID = 1482962712844828713      # Вторая роль принятых
AFK_ROLE_ID = 1489293268008042639             # Роль для афк




# Файл хранения заявок
APPLICATIONS_FILE = 'data/applications.json'