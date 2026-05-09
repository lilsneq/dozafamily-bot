import discord
from discord import app_commands

# Импортируем настройки и функции работы с JSON из ваших модулей
from config.settings import CHANNEL_FOR_CAPT
from utils.storage import start_new_capt_id
from models.application_button import CaptPanelButtons

# Создаем слэш-команду и привязываем её к глобальному дереву бота
@app_commands.command(name="new_capt", description="Создать новую панель капта (автоматически увеличит номер капта)")
@app_commands.checks.has_permissions(administrator=True)
async def new_capt_command(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    new_id = start_new_capt_id()

    guild = interaction.guild
    capt_panel_channel = guild.get_channel(CHANNEL_FOR_CAPT)

    if not capt_panel_channel:
        await interaction.followup.send("❌ Канал для каптов не найден в конфигурации бота.", ephemeral=True)
        return

    try:



        capt_embed = discord.Embed(
            title=f'👳🏿‍♀️ ЗАЯВКА НА КАПТ №{new_id}',
            description=(
                'НАЖМИТЕ НА ПРИНЯТЬ, ЕСЛИ ВЫ ХОТИТЕ УЧАСТВОВАТЬ В КАПТЕ\n'
                'НАЖМИТЕ НА УДАЛИТЬ, ЕСЛИ ХОТИТЕ, ЧТОБЫ ВСЕ УЧАСТНИКИ УДАЛИЛИСЬ\n\n'
                '**СПИСОК УЧАСТНИКОВ (0):**\n*Список пуст*'
            ),
            color=discord.Color.red()
        )

        view = CaptPanelButtons()

        await capt_panel_channel.send(embed=capt_embed, view=view)

        await interaction.followup.send(
            f"✅ Успешно открыта панель для Капта №{new_id} в канале {capt_panel_channel.mention}!",
            ephemeral=True
        )

        from events.bot_events import send_log
        await send_log(
            guild,
            f'🔧 **Панель капта создана вручную командой**\nМодератор: {interaction.user.mention}\nНомер капта: **№{new_id}**\nКанал: {capt_panel_channel.mention}',
            discord.Color.orange()
        )

    except discord.Forbidden:
        await interaction.followup.send(
            "❌ Недостаточно прав! Убедитесь, что у бота есть право на управление сообщениями в этом канале.",
            ephemeral=True
        )
    except Exception as e:
        print(f"Ошибка при выполнении команды /new_capt: {e}")
        await interaction.followup.send(f"❌ Системная ошибка при создании панели: {e}", ephemeral=True)
