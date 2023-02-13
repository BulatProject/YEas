import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from check_availability import EXAMPLES, CLEAN_LINK, ERRORS, Checker
from get_mp3 import BAN_LIST, CONVERSION, WEBM, MP3, CONVERSION_ERROR, DOWNLOADING_ERROR, Downloader
from prepare_text import COMMA_MESSAGE_ERROR, HYPHEN, SYMBOLS_ERROR, RANGE_ERROR, Preparator
from pytube import Playlist
from os import remove

START = 'Перед использоваием ОБЯЗАТЕЛЬНО прочтите описание и инструкцию по использованию бота, введя: "/help" и "/info".'
HELP = \
'''Данный бот предназначен для скачивания песен с YouTube, но его можно использовать и для скачивания аудиоряда из любого видео.
Бот скачивает аудиоряд в формате webm, а затем конвертирует в mp3, добавляя теги.

Скачивать песни можно как по одной, так группой из плейлистов.

Из-за особенностей библиотеки FFMPEG, которая используется для конвертации файлов, название файла может не совпадать с названием видео.

Если в названии видео присутстуют символы из следующего списка: '/', '\\', ':', '*', '?', '<', '>', '|', '"', "'", то файл точно будет иметь другое название.
Воздержитесь от скачивания видео с нестандартными символами в названии.

ВАЖНО!
Бот автоматически убирает из названия песни следующие комбинации символов (в теги они тоже не попадут):
'(Official Video)', '(Official Music Video)', '(Official Audio)', \
'[Official Music Video]', '[Official Video]', '[Official Audio]', \
'(Lyrics)', '(lyrics)', '(Lyric Video)', '(Official Lyrics Video)', \
'(Official Video)', '(High Quality)', 'Lyrics', 'lyrics'.

Также он заполняет теги "исполнители" и "название".
Если в названии видео нет символа "-", то название видео становится названием трека, а название канала - именем исполнителя.
В противном случае он делит название видео пополам, и левая часть становится именем исполнителя, а правая - названием трека.

После скачивания, соответственно, советую подкорректировать теги, если это имеет для вас значение.

Чтобы посмотреть доступные команды, наберите /commands.
'''

COMMANDS = \
'''
/start - запустить бота.
/info - инструкция по работе с ботом.
/help - узнать основную информацию о боте (перед использование ОБЯЗАТЕЛЬНО ознакомьтесь).
/commands - получить эту инструкцию.
'''

INFO = \
'''ВАЖНО. Если видео, аудиоряд которого вы хотите скачать, имеет возрастные или иные ограничения, то видео скачано не будет!

Использовать бота просто:
Введите ссылку на видео и нажмите на кнопку "Один трек", если хотите скачать аудиоряд из видео.

Пример:
https://youtu.be/Z6kNQEzQJpA


Если же вы хотите скачать видео из плейлиста, то инструкция следующая:
Вы должны ввести диапазон (в нём должно быть не больше 20 чисел), в котором находятся треки, что вы хотите скачать, и ссылку на плейлист.

Пример:
1-21, https://youtube.com/playlist?list=КОДПЛЕЙЛИСТА

В данном случае скачаны будут первые 20 песен из текущего плейлиста.
Если в вашем диапазоне больше 20 песен, то песни скачаны не будут.
Если в плейлисте меньше песен, нежели вы указали, песни скачаны не будут.

К сожалению, каждый раз вам придётся присылать ссылку и диапазон заново.
Возможно, в будущем это неудобство будет устранено.
'''

WRONG_COMMAND = "Эта комманда не поддерживается."

ILOVEYOU = 'Обнимаю и целую. =3'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=START)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP)

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=COMMANDS)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=INFO)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=WRONG_COMMAND)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check = check_url(update.message.text)
    if not check[0]:
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=check[1])
    result = run_all(check[1], str(update.effective_chat.id))
    print(result)
    if not result[0]:
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=result[1])    
    await context.bot.send_document(chat_id=update.effective_chat.id, document=result[1])
    remove(result[1])

def check_url(text):
    handling = Checker(text)
    if not handling.base_check[0]:
        return handling.base_check
    response = handling.check_status_code(handling.base_check[1])
    if not response[0]:
        return response
    return handling.check_access(response[1])

def run_all(yt, id):
    download = download_song(yt, id)
    if not download[0]:
        return download
    convert = convert_file(download[1])
    return convert

# Возвращает кортеж (True/False, имя ошибки/ссылку на экземпляр класса)
def download_song(response, id):
    download = Downloader(response, id)
    get = download.download()
    return get

# Возвращает кортеж (True/False, имя ошибки/путь к файлу)
def convert_file(download):
    file_path = download.convert()
    return file_path

async def iloveyou(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ILOVEYOU)

#TODO Проход по списку плейлиста, кнопки и превью в чате. Плюс вынести текст в отдельный файл.
def download_playlist():
    pass

if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    commands_handler = CommandHandler('commands', commands)
    info_handler = CommandHandler('info', info)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    love = CommandHandler('iloveyou', iloveyou)

    application.add_handler(message_handler)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(commands_handler)
    application.add_handler(info_handler)
    application.add_handler(love)

    application.add_handler(unknown_handler)

    application.run_polling()