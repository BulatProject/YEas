import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from check_availability import EXAMPLES, CLEAN_LINK, ERRORS, Checker
from get_mp3 import BAN_LIST, CONVERSION, WEBM, MP3, CONVERSION_ERROR, DOWNLOADING_ERROR, Downloader
from prepare_text import COMMA_MESSAGE_ERROR, HYPHEN, SYMBOLS_ERROR, RANGE_ERROR, LENGHT_ERROR, INSTRUCTION_ERROR, STARTING_WORDS, NO_FIRST_NUM_ERROR, RANGE_TOO_BIG, Preparator
from pytube import Playlist
from os import remove, listdir, path
from TOK import TOKEN
import random

START = 'Перед использованием ОБЯЗАТЕЛЬНО прочтите описание и инструкцию по использованию бота, введя: "/help" и "/info".'
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
f'''ВАЖНО. Если видео, аудиоряд которого вы хотите скачать, имеет возрастные или иные ограничения, то видео скачано не будет!

Использовать бота просто:
Введите: "Трек, ССЫЛКА_НА_ВИДЕО", - и отправьте сообщение, если хотите скачать аудиоряд из одного видео.

Пример:
Трек, https://youtu.be/Z6kNQEzQJpA

{CLEAN_LINK}

Если же вы хотите скачать видео из плейлиста, то инструкция следующая:
Введите: "Лист, ДИАПАЗОН, ССЫЛКА_НА_ППЛЕЙЛИСТ".
Диапазон, в котором находятся треки, должен быть не больше 20.

Пример:
Лист, 1-21, https://youtube.com/playlist?list=КОДПЛЕЙЛИСТА

В данном случае скачаны будут первые 20 песен из указанного плейлиста.
Если в вашем диапазоне больше 20 песен, то песни скачаны не будут.
Если в плейлисте меньше песен, нежели в диапазоне, что вы указали, песни скачаны не будут.

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

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP, disable_web_page_preview=True)

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=COMMANDS)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=INFO, disable_web_page_preview=True)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=WRONG_COMMAND)

async def random_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memes = listdir('memes')
    i = random.randrange(len(memes))    
    meme_to_post = path.join('memes', memes[i])
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=meme_to_post)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = str(update.message.text)
    first_check = Preparator(message)
    if not first_check.results[0]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=first_check.results[1], disable_web_page_preview=True)
        return
    shortened_message = message[5:].strip()
    if first_check.results[1] == STARTING_WORDS[1]:
        cleaned_message = first_check.divide_n_clean_message(shortened_message)
        if not cleaned_message[0]:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=cleaned_message[1])
            return
        cleaned_range = first_check.check_range(cleaned_message[1])
        if not cleaned_range[0]:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=cleaned_range[1])
            return
        playlist = first_check.get_playlist(cleaned_message[2])
        if cleaned_range[1][0] - cleaned_range[1][1] > len(playlist):
            await context.bot.send_message(chat_id=update.effective_chat.id, text=RANGE_TOO_BIG)
            return
        for song in playlist[cleaned_range[1][0]:cleaned_range[1][1]]:
            final_result = pre_download(update, song)
            if not final_result[0]:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=final_result[1], disable_web_page_preview=True)
                continue;
            await context.bot.send_document(chat_id=update.effective_chat.id, document=final_result[1])
            remove(final_result[1])
        return
    final_result = pre_download(update, shortened_message)
    if not final_result[0]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=final_result[1], disable_web_page_preview=True)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=final_result[1])
    remove(final_result[1])

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


#TODOErrorerror(update, context):\nlogger.warning("Update '%s' caused error '%s'", update, context.error)
#Все манипуляции с файлами перенесены в эту функцию.
def pre_download(update, message):
    check = check_url(message)
    if not check[0]:
        return check
    result = run_all(check[1], str(update.effective_chat.id))
    if not result[0]:
        return result
    return (True, result[1])


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    commands_handler = CommandHandler('commands', commands)
    info_handler = CommandHandler('info', info)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    love = CommandHandler('iloveyou', iloveyou)
    meme = CommandHandler('meme', random_meme)

    application.add_handler(message_handler)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(commands_handler)
    application.add_handler(info_handler)
    application.add_handler(love)
    application.add_handler(meme)

    application.add_handler(unknown_handler)

    application.run_polling()