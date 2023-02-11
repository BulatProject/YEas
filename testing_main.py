import requests
import os
import telegram
from telegram.ext import Updater, filters, MessageHandler, CommandHandler
from check_availability import EXAMPLES, CLEAN_LINK, ERRORS, Checker
from get_mp3 import BAN_LIST, CONVERSION, WEBM, MP3, CONVERSION_ERROR, DOWNLOADING_ERROR, Downloader
from pytube import YouTube
import subprocess
from os import remove, rename
import os.path as path
import eyed3
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def error(update, context):
    logger.warning("Update '%s' caused error '%s'", update, context.error)

#TODO Кнопки: Один трек, плейлист.

API_TOKEN = 'TOKEN'
START = 'Выбери команду.\nПрочти описание, введя: "\\help".'
HELP = \
'''Данный бот предназначен для скачивания песен с YouTube, но его можно использовать и для скачивания аудиоряда из любого видео.
Бот скачивает аудиоряд в формате webm, а затем конвертирует в mp3, добавляя теги.

Скачивать песни можно как по одной, так группой из плейлистов.

Название видео становится названием трека, а название канала именем исполнителя.
После скачивания, соответственно, советую подкорректировать инфомацию, если это имеет для вас значение.

Из-за особенностей библиотеки FFMPEG, которая используется для конвертации файлов, название файла может не соответствовать названию видео.
Если в названии видео присутстуют символы из следующего списка: '/', '\\', ':', '*', '?', '<', '>', '|', '"', "'", то файл точно будет иметь другое название.
Воздержитесь от скачивания видео с нестандартными символами в названии.

ВАЖНО. Если в названии видео есть иероглифы, то название файла будет пустым.
Поэтому не передавайте боту плейлисты, в которых больше одной песни с иероглифами в названии подряд.

Чтобы посмотреть доступные команды, нберите \commands.
'''

COMMANDS = \
'''
\start - запустить бота.
\help - узнать основную информацию о боте.
\commands - получить эту инструкцию.
'''


class My:
    def __init__(self):
        # Бот ответственен за отправку песен!
        self.bot = telegram.Bot(token=API_TOKEN)
        self.updater = Updater(token=API_TOKEN)
        # Step 4: Start the bot
        self.dispatcher = self.updater.dispatcher

        # Ответ на команды \start, \help, \commands.
        self.dispatcher.add_handler(CommandHandler('start', self.handle_start))
        self.dispatcher.add_handler(CommandHandler('help', self.handle_help))
        self.dispatcher.add_handler(CommandHandler('help', self.handle_commands))

        # Задаём ответ на любое текстовое сообщение.
        self.dispatcher.add_handler(MessageHandler(filters.text, self.communicate))
        self.dispatcher.add_handler(MessageHandler(filters.command, self.unknown))
        # Добавляем логгирование ошибок.
        self.dispatcher.add_error_handler(error)

    # Отправляет регулярные запросы к серверу Telegram и проверяет обновления.
        self.updater.start_polling()


    def communicate(self, update, context):
        chat = update.effective_chat

        # Моё.
        result = self.respond_message(update.message.text)
        if result[0]:
            # Файл отправляется пользоватею, а затем удаляется.
                # Добавить пересылку файла в чат с последующим удалением.
                # Send the file to the chat
                # bot.send_document(chat_id=update.message.chat_id, document=open(file_name, "rb"))
            pass
        else:
            # Сообщение об ошибке отправлется пользователю.
            context.bot.send_message(chat_id=chat.id, text=result[1])

#TODO Движущееся окно по списку.
    def respond_message(self, text):
        if text == 'Один трек':
            # Что делать, когда нажали на кнопку?
            pass
        self.check_url(text)

    def check_url(self, text):
        handling = Checker(text)
        self.response = handling.check_status_code()
        if type(self.response) is str:
            return [False, self.response]
        else:
            self.download_song()

    def download_song(self):
            self.download = Downloader(self.response)
            get = self.download.download()
            if type(get) is str:
                return [False, get]
            else:
                self.convert_file()

    def convert_file(self):
            file_path = self.download.convert()
            if file_path.startswith('Произошла'):
                return [False, file_path]
            else:
                return [True, file_path]

    def handle_start(self, update, context):
        chat = update.effective_chat
        buttons = [telegram.KeyboardButton('Один трек')], [telegram.KeyboardButton('Плейлист')]
        reply = telegram.ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        context.bot.send_message(chat_id=chat.id, text=START, reply_markup=reply)

    def handle_help(self, update, context):
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text=HELP)

    def handle_commands(self, update, context):
        chat = update.effective_chat
        context.bot.send_message(chat_id=chat.id, text=COMMANDS)

    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                text="Такая команда не поддерживается.")



