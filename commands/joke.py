"""КОМАНДА В ЧАТ ЧТОБЫ ПОЛУЧИТЬ ОТВЕТ ОТ БОТА"""


import discord
import random
from discord import app_commands



def setup_joke_commands(bot):
    """Настройка команд для получения iq"""
    random_num = random.randint(1, 100)


    @bot.tree.command(name='iq', description='Показать свой iq')
    async def iq_command(interaction: discord.Interaction, user: discord.Member):
        random_num = random.randint(1, 100)

        embed = discord.Embed(
                title=f'📈IQ пользователя {user.name}',
                description=f'**Пользователь:** {user.mention}\n**IQ:** {random_num}',
                color=discord.Color.blue()
            )
        embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=False)



