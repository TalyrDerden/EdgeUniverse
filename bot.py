import random

import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = '/'

# Инициализация бота с префиксом команд
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot connected as {bot.user}')


# Команда для броска кубиков в стиле PBTA
@bot.tree.command(name='roll', description='Бросает 2d6 для PBTA и выводит результат.')
async def roll(interaction: discord.Interaction, modifier: int = 0):
    rolls = Rolls()
    rez = result(rolls.total,"","","")
    await interaction.response.send_message(response(interaction.user.display_name,rolls,modifier,rez))


@bot.tree.command(name='fdanger', description='Смотришь в лицо опасности')
async def fdanger(interaction: discord.Interaction, modifier: int = 0):
    rolls = Rolls()
    rez = result(rolls.total, "Ты избегаешь угрозы; получи возможность"
                 , "Получи возможность но столкнись со сложным выбором или испытай перегрузку"
                 , "Испытай перегрузку")
    await interaction.response.send_message(response(interaction.user.display_name,rolls,modifier,rez))


@bot.tree.command(name='hyourself', description='Держишь себя в руках')
async def hyourself(interaction: discord.Interaction, modifier: int = 0):
    rolls = Rolls()
    rez = result(rolls.total, "ты сжимаешь свою волю в кулак: получи возможность"
                 , "ты ещё контролируешь себя, но испытай перегрузку"
                 , "ты теряешь контроль над собой")
    await interaction.response.send_message(response(interaction.user.display_name,rolls,modifier,rez))

@bot.tree.command(name="takeсover", description="Укрываешься")
async def takeсover(interaction: discord.Interaction, modifier: int = 0):
    rolls = Rolls()
    rez = result(rolls.total, "выбери 2:\n"
        "• Переведи дух и избавься от Состояния;\n"
        "• Получи возможность;\n"
        "• Ты можешь находиться в укрытии долго;\n"
        "• Ты можешь укрыть ещё кого-то.\n"
                 , "выбери 1\n"
                   "• Переведи дух и избавься от Состояния;\n"
                   "• Получи возможность;\n"
                   "• Ты можешь находиться в укрытии долго;\n"
                   "• Ты можешь укрыть ещё кого-то.\n"
                 , "испытай перегрузку")
    await interaction.response.send_message(response(interaction.user.display_name,rolls,modifier,rez))

class Rolls:
    def __init__(self):
        self.roll1 = random.randint(1, 6)
        self.roll2 = random.randint(1, 6)
        self.total = self.roll1 + self.roll2

def result(total, very, good, no):
    if total >= 10:
        return (f"УСПЕХ.\n {very}")
    elif 7 <= total <= 9:
        return (f"Частичный успех.\n{good}")
    else:
        return (f"Провал.\n{no}")

def response(name, rolls=None, modifier=None, rez=None):
    return (f"{name} бросили 2d6: {rolls.roll1} + {rolls.roll2} + {modifier} = {rolls.total + modifier}\n"
        f"Результат: {rez}")

bot.run(TOKEN)
