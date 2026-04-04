"""Модуль для управления ролями и никнеймами"""
import discord
from config.settings import (
    APPLICANT_ROLE_ID,
    ACCEPTED_ROLE_1_ID,
    ACCEPTED_ROLE_2_ID,
    AFK_ROLE_ID

)
# from models.application_modal import


async def set_applicant_nickname(member, full_name: str, ooc_name: str):
    """Установить никнейм заявителя"""
    try:
        new_nickname = f"{full_name} | {ooc_name}"
        await member.edit(nick=new_nickname)
        return True
    except Exception as e:
        print(f"Ошибка при изменении никнейма: {e}")
        return False


async def give_afk_role(member):
    """Выдаь роль АФК"""
    try:
        role = member.guild.get_role(AFK_ROLE_ID)
        if role:
            await member.add_roles(role)
            return True
    except Exception as e:
        print(f"Ошибка при выдаче роли заявителя: {e}")
    return False


async def give_applicant_role(member):
    """Выдать роль заявителя"""
    try:
        role = member.guild.get_role(APPLICANT_ROLE_ID)
        if role:
            await member.add_roles(role)
            return True
    except Exception as e:
        print(f"Ошибка при выдаче роли заявителя: {e}")
    return False


async def give_accepted_roles(member):
    """Выдать роли принятому"""
    try:
        role1 = member.guild.get_role(ACCEPTED_ROLE_1_ID)

        if role1:
            await member.add_roles(role1)

        return True
    except Exception as e:
        print(f"Ошибка при выдаче ролей принятого: {e}")
    return False


async def remove_applicant_role(member):
    """Убрать роль заявителя"""
    try:
        role = member.guild.get_role(APPLICANT_ROLE_ID)
        if role:
            await member.remove_roles(role)
            return True
    except Exception as e:
        print(f"Ошибка при снятии роли заявителя: {e}")
    return False


async def setup_new_member(member):
    """Настройка нового участника"""
    await give_applicant_role(member)




