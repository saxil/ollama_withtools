import telebot

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

    def start(self, on_message_callback):
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            self.bot.reply_to(message, "Hello! AI Agent is active. Send me commands.")

        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            response = on_message_callback(message.text)
            self.bot.reply_to(message, response)

        self.bot.infinity_polling()
