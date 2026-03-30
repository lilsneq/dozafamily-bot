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

# ID ролей
APPLICANT_ROLE_ID = 1236152539968438312       # Роль для подающих заявки
ACCEPTED_ROLE_1_ID = 1236152539968438312      # Первая роль принятых
ACCEPTED_ROLE_2_ID = 1471969251018412053      # Вторая роль принятых

# Файл хранения заявок
APPLICATIONS_FILE = 'data/applications.json'