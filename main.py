import discord
from discord.ext import commands
import requests
from io import BytesIO
from PIL import Image
import cairosvg

# Инициализация бота
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="", intents=intents)

# Событие, когда бот готов
@bot.event
async def on_ready():
    print(f'{bot.user} подключился к Discord!')
    await bot.tree.sync()
    print(f"Команды приложения синхронизированы!")

# Создание команды приложения
@bot.tree.command(name="hello", description="Приветствие")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Привет!")

# Создание команды check
@bot.tree.command(name="check", description="Проверка пользователя")
async def check(interaction: discord.Interaction, user: str):
    url = f"https://stdstatistics.onrender.com/generate-svg?username={user}"  # Замените на ваш URL
    response = requests.get(url)
    if response.status_code == 200:
        # Конвертируем SVG в PNG
        svg_data = response.content
        png_data = cairosvg.svg2png(svg_data)
        # Создаем файловый объект
        file = BytesIO(png_data)
        # Отправляем файл в чат
        await interaction.response.send_message(file=discord.File(file, f"{user}.png"))
    else:
        await interaction.response.send_message("Ошибка при загрузке SVG")

# Создание команды checkbb
@bot.tree.command(name="bbcheck", description="Проверка пользователя (альтернативный URL)")
async def bbcheck(interaction: discord.Interaction, user: str):
    url = f"https://stdstatistics.onrender.com/generatebb-svg?username={user}"  # Замените на ваш альтернативный URL
    response = requests.get(url)
    if response.status_code == 200:
        # Конвертируем SVG в PNG
        svg_data = response.content
        png_data = cairosvg.svg2png(svg_data)
        # Создаем файловый объект
        file = BytesIO(png_data)
        # Отправляем файл в чат
        await interaction.response.send_message(file=discord.File(file, f"{user}.png"))
    else:
        await interaction.response.send_message("Ошибка при загрузке SVG")

# Токен бота
TOKEN = "TOKEN"

bot.run(TOKEN)
