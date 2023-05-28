import requests
import json
import telebot


# Класс для обработки исключений при работе с API
class APIException(Exception):
    def __init__(self, message):
        self.message = message

# Класс для работы с API валютного курса
class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException('Невозможно конвертировать одинаковые валюты.')

        try:
            base = base.upper()
            quote = quote.upper()
            amount = float(amount)

            url = f'https://api.exchangerate-api.com/v4/latest/{base}'
            response = requests.get(url)
            data = json.loads(response.text)

            if quote in data['rates']:
                exchange_rate = data['rates'][quote]
                result = exchange_rate * amount
                return result
            else:
                raise APIException('Неправильно указана валюта.')

        except ValueError:
            raise APIException('Неправильно указано количество.')

# Конфиг с токеном Telegram-бота
class Config:
    TOKEN = 'я не знал нужен ли токен но если нужен то пожалуйста напишите об этом когда будете проверять работу'

# Инициализация Telegram-бота
bot = telebot.TeleBot(Config.TOKEN)

# Обработчик команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = "Привет! Я бот для конвертации валют.\n\n"
    instructions += "Чтобы узнать цену валюты, отправь сообщение в формате:\n"
    instructions += "<имя валюты, цену которой ты хочешь узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n\n"
    instructions += "Например:\n"
    instructions += "USD RUB 100\n\n"
    instructions += "Для получения списка доступных валют используй команду /values."

    bot.reply_to(message, instructions)

# Обработчик команды /values
@bot.message_handler(commands=['values'])
def send_currency_values(message):
    currency_values = "Доступные валюты:\n"
    currency_values += "- USD (Доллар США)\n"
    currency_values += "- EUR (Евро)\n"
    currency_values += "- RUB (Российский рубль)"

    bot.reply_to(message, currency_values)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        base, quote, amount = message.text.split()
        result = CurrencyConverter.get_price(base, quote, amount)
        response = f"{amount} {base} = {result} {quote}"
    except ValueError:
        response = "Ошибка: неправильный формат ввода. Пожалуйста, введите данные в формате <валюта1> <валюта2> <количество>."
    except APIException as e:
        response = f"Ошибка: {str(e)}"

    bot.reply_to(message, response)

# Запуск бота
bot.polling()
