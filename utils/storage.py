"""Модуль для работы с хранением заявок"""
import json
import os
from config.settings import APPLICATIONS_FILE

# Хранилище заявок
applications = {}
application_counter = 0


def load_applications():
    """Загрузка заявок из файла"""
    global applications, application_counter
    try:
        if os.path.exists(APPLICATIONS_FILE):
            with open(APPLICATIONS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                applications = data.get('applications', {})
                application_counter = data.get('counter', 0)
            print(f'Загружено {len(applications)} заявок')
        else:
            # Создаем директорию data если её нет
            os.makedirs(os.path.dirname(APPLICATIONS_FILE), exist_ok=True)
            print('Файл заявок не найден, будет создан новый')
    except Exception as e:
        print(f"Ошибка при загрузке заявок: {e}")


def save_applications():
    """Сохранение заявок в файл"""
    try:
        # Создаем директорию если её нет
        os.makedirs(os.path.dirname(APPLICATIONS_FILE), exist_ok=True)
        
        with open(APPLICATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'applications': applications,
                'counter': application_counter
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении заявок: {e}")


def get_next_app_id():
    """Получить следующий ID заявки"""
    global application_counter
    application_counter += 1
    return application_counter


DATA_FILE = 'data/sub.json'

def add_application_sub(data):
    """Сохраняет данные о подписке в JSON файл"""

    # Создаем папку data, если её нет
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    # 1. Читаем текущие данные
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                all_data = json.load(f)
                if not isinstance(all_data, list):
                    all_data = []
            except json.JSONDecodeError:
                all_data = []
    else:
        all_data = []

    # 2. Добавляем новую запись
    all_data.append(data)

    # 3. Сохраняем обратно
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)


def add_application(app_data):
    """Добавить заявку"""
    app_id = str(app_data['id'])
    applications[app_id] = app_data
    save_applications()


def get_application(app_id):
    """Получить заявку по ID"""
    return applications.get(str(app_id))


def update_application(app_id, updates):
    """Обновить заявку"""
    app_id_str = str(app_id)
    if app_id_str in applications:
        applications[app_id_str].update(updates)
        save_applications()
        return True
    return False