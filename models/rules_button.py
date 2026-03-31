"""Кнопки для правил сервера с большим изображением"""
import discord


class RulesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(discord.ui.Button(
            label='Правила сервера',
            style=discord.ButtonStyle.link,
            url='https://docs.google.com/document/d/1eZWV6J8NwFgPeK_vhD6woovznuvxj10Gwcv6-QmnNow/edit?tab=t.0'
        ))


async def send_rules(ctx):
    url = 'https://i.pinimg.com/1200x/d4/c9/cb/d4c9cbbd34bcb79302cfcd18a5f641fd.jpg'

    embed = discord.Embed(title="Правила сервера", description="Пожалуйста, ознакомьтесь с правилами:")
    embed.set_image(url=url)  # Устанавливаем ту самую большую картинку

    await ctx.send(embed=embed, view=RulesView())
