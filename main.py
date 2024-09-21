import discord
from discord import app_commands
from discord.ext import commands
import requests

# Замените 'your_token' на токен вашего Discord бота
TOKEN = ''
GUILD_ID = '1258464202214080595'  # ID вашего сервера (если бот предназначен для одного сервера)

# Инициализируем бота
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Регистрируем команду /check через app_commands
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=GUILD_ID))  # Синхронизация команд с сервером


client = MyClient()

# Определяем команду /check
@client.tree.command(name="checks", description="Проверить информацию по общей статистике пользователя", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(username="Ник пользователя на площадке Standoff365, по которому нужно получить информацию")
async def check(interaction: discord.Interaction, username: str):
    # URL API, подставляем username
    api_url = f"https://api.standoff365.com/api/scoring-mgr/scoring/total/{username}"

    try:
        # Выполняем GET-запрос
        response = requests.get(api_url)

        # Проверяем успешность запроса
        if response.status_code == 200:
            data = response.json()  # Преобразуем ответ в JSON

            # Извлекаем данные из JSON (зависит от структуры данных)
            total_rating = data.get('position', 'Нет данных')
            crPosition = data.get('crPosition', 'Нет данных')
            bbPosition = data.get('bbPosition', 'Нет данных')
            total = data.get('total', 'Нет данных')
            bbTotal = data.get('bbTotal', 'Нет данных')
            crTotal = data.get('crTotal', 'Нет данных')
            bbReportsCount = data.get('bbReportsCount', 'Нет данных')
            crReportsCount = data.get('crReportsCount', 'Нет данных')
            crVulnerability = data.get('crVulnerability', 'Нет данных')
            crBusinessRisk = data.get('crBusinessRisk', 'Нет данных')
            groupName = data.get('groupName', 'Нет данных')
            groupLogo = data.get('groupLogo', 'Нет данных')
            if groupLogo is not None:
                urllogo = 'https://api.standoff365.com/images/200_200/' + groupLogo

            # Создаем embed сообщение
            embed = discord.Embed(title=f"Информация по игроку {username}", color=0x00ff00)
            embed.add_field(name="Общий рейтинг", value=total_rating, inline=True)
            embed.add_field(name="Рейтинг на киберполигоне", value=crPosition, inline=True)
            embed.add_field(name="Рейтинг багбаунти", value=bbPosition, inline=True)
            embed.add_field(name="Количество баллов", value=total, inline=True)
            embed.add_field(name="Количество баллов багбанути", value=bbTotal, inline=True)
            embed.add_field(name="Количество баллов киберполигона", value=crTotal, inline=True)
            embed.add_field(name="Количество отчетов багбаунти", value=bbReportsCount, inline=True)
            embed.add_field(name="Количество отчетов киберполигона", value=crReportsCount, inline=True)
            embed.add_field(name="Баллы за уязвимости киберполигона", value=crVulnerability, inline=False)
            embed.add_field(name="Баллы за недопустимые события", value=crBusinessRisk, inline=True)
            embed.add_field(name="Команда", value=groupName, inline=True)
            if groupLogo is not None:
                embed.set_thumbnail(url=urllogo)

            # Отправляем embed сообщение в канал
            await interaction.response.send_message(embed=embed)
        else:
            # Если статус-код не 200, выводим ошибку
            await interaction.response.send_message(f"Пользователь не найден, либо это внутренняя ошибка. Статус код: {response.status_code}", ephemeral=True)

    except requests.exceptions.RequestException as e:
        # Если произошла ошибка с запросом
        await interaction.response.send_message(f"Пользователь не найден, либо это внутренняя ошибка. Статус код: {response.status_code}", ephemeral=True)


@client.tree.command(name="bbchecks", description="Проверить информацию по багбаунти статистике пользователя", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(username="Ник пользователя на площадке Standoff365, по которому нужно получить информацию")
async def check(interaction: discord.Interaction, username: str):
    # URL API, подставляем username
    bbapi_url = f"https://api.standoff365.com/api/bug-bounty/metrics/user/{username}"
    api_url = f"https://api.standoff365.com/api/scoring-mgr/scoring/total/{username}"


    try:
        # Выполняем GET-запрос
        response = requests.get(api_url)
        bbresponse = requests.get(bbapi_url)

        # Проверяем успешность запроса
        if (response.status_code == 200 and bbresponse.status_code==200):
            data = response.json()  # Преобразуем ответ в JSON

            # Извлекаем данные из JSON (зависит от структуры данных)
            bbPosition = data.get('bbPosition', 'Нет данных')
            groupName = data.get('groupName', 'Нет данных')
            groupLogo = data.get('groupLogo', 'Нет данных')
            if groupLogo is not None:
                urllogo = 'https://api.standoff365.com/images/200_200/' + groupLogo


            bbdata = bbresponse.json()

            # Извлекаем данные из JSON (зависит от структуры данных)
            signal = bbdata.get('signal', 'Нет данных')
            impact = bbdata.get('impact', 'Нет данных')
            reportsTotal = bbdata.get('reportsTotal', 'Нет данных')
            reportsFinished = bbdata.get('reportsFinished', 'Нет данных')
            reportsInProgress = bbdata.get('reportsInProgress', 'Нет данных')
            reportsAccepted = bbdata.get('reportsAccepted', 'Нет данных')
            reportsInformational = bbdata.get('reportsInformational', 'Нет данных')
            reportsDuplicate = bbdata.get('reportsDuplicate', 'Нет данных')
            reportsOutOfScope = bbdata.get('reportsOutOfScope', 'Нет данных')
            reportsRejected = bbdata.get('reportsRejected', 'Нет данных')
            reportsAbuse = bbdata.get('reportsAbuse', 'Нет данных')


            # Создаем embed сообщение
            embed = discord.Embed(title=f"Информация по игроку {username}", color=0x00ff00)
            embed.add_field(name="Рейтинг багбаути", value=bbPosition, inline=True)
            embed.add_field(name="Качество отчетов", value=signal, inline=True)
            embed.add_field(name="Польза", value=impact, inline=True)
            embed.add_field(name="Количество отчетов", value=reportsTotal, inline=True)
            embed.add_field(name="Отчетов закрыто", value=reportsFinished, inline=True)
            embed.add_field(name="Отчетов в прогрессе", value=reportsInProgress, inline=True)
            embed.add_field(name="Отчетов принято", value=reportsAccepted, inline=True)
            embed.add_field(name="Информативов", value=reportsInformational, inline=True)
            embed.add_field(name="Дубликатов", value=reportsDuplicate, inline=False)
            embed.add_field(name="Вне скоупа", value=reportsOutOfScope, inline=True)
            embed.add_field(name="Отклонено", value=reportsRejected, inline=True)
            embed.add_field(name="Спам отчетов", value=reportsAbuse, inline=True)

            embed.add_field(name="Команда", value=groupName, inline=True)
            if groupLogo is not None:
                embed.set_thumbnail(url=urllogo)

            # Отправляем embed сообщение в канал
            await interaction.response.send_message(embed=embed)
        else:
            # Если статус-код не 200, выводим ошибку
            await interaction.response.send_message(f"Пользователь не найден, либо это внутренняя ошибка. Статус код: {response.status_code}", ephemeral=True)

    except requests.exceptions.RequestException as e:
        # Если произошла ошибка с запросом
        await interaction.response.send_message(f"Пользователь не найден, либо это внутренняя ошибка. Статус код: {response.status_code}", ephemeral=True)



# Запуск бота
client.run(TOKEN)
