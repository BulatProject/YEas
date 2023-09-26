from os import remove, listdir, path, getenv
import logging
import random

from pytube import YouTube
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

from check_availability import Checker
from get_mp3 import Downloader
from prepare_text import Preparator
from TEXTS import *


load_dotenv()
TOKEN = getenv("TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger("YEasy")
logger.info("Logging started")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=START)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP, disable_web_page_preview=True)

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=COMMANDS)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=INFO, disable_web_page_preview=True)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=WRONG_COMMAND)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning("Update '%s' caused error '%s'", update, context.error)

# Easer egg
async def iloveyou(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ILOVEYOU)

# Easer egg
async def random_meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    memes = listdir('memes')
    i = random.randrange(len(memes))
    meme_to_post = path.join('memes', memes[i])
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=meme_to_post)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update is None:
        return None
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Запрос обрабатывается, ожидайте.')
    message = str(update.message.text)
    first_check = Preparator(message) # Checking if message starts from command name (single track or playlist)
    if not first_check.results[0]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=first_check.results[1], disable_web_page_preview=True)
        return None
    shortened_message = message[5:].strip() # Slicing command name from text.
    if first_check.results[1] == STARTING_WORDS[1]: # Checking command name again.
        playlist = prepare_playlist(first_check, shortened_message)
        if not playlist[0]:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=playlist[1], disable_web_page_preview=True)
            return None
        cleaned_range = playlist[2]
        for song in playlist[1][cleaned_range[1][0]:cleaned_range[1][1]]:
            final_result = pre_download(update, song)
            if not final_result[0]:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=final_result[1], disable_web_page_preview=True)
            else:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=final_result[1])
                remove(final_result[1])
        return None
    final_result = pre_download(update, shortened_message)
    if not final_result[0]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=final_result[1], disable_web_page_preview=True)
    else:
        try:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=final_result[1])
            logger.info(f"\"{final_result[1][10:]}\" has been sent")
        except Exception as err:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Возникла ошибка при отправке файла.')
            logger.exception(err)
        finally:
            remove(final_result[1])


def prepare_playlist(first_check: Preparator, shortened_message: str) -> tuple[bool, list, str]:
    cleaned_message = first_check.divide_n_clean_message(shortened_message)
    if not cleaned_message[0]:
        return (False, cleaned_message[1])
    cleaned_range = first_check.check_range(cleaned_message[1])
    if not cleaned_range[0]:
        return (False, cleaned_range[1])
    playlist = first_check.get_playlist(cleaned_message[2])
    if cleaned_range[1][1] > len(playlist):
        return (False, RANGE_TOO_BIG)
    else:
        return (True, playlist, cleaned_range)


def check_url(text: str) -> tuple[bool, str | YouTube]:
    handling = Checker(text)
    if not handling.base_check[0]:
        return handling.base_check
    response = handling.check_status_code(handling.base_check[1])
    if not response[0]:
        return response
    return handling.check_access(response[1])


def run_all(yt: tuple[bool, YouTube], id: str) -> tuple[bool, str]:
    download = download_song(yt, id)
    if not download[0]:
        return download
    convert = convert_file(download[1])
    return convert


def download_song(response: tuple[bool, str], id: str) -> tuple[bool, str | Downloader]:
    download = Downloader(response, id)
    get = download.download()
    return get


def convert_file(download: Downloader) -> tuple[bool, str]:
    file_path = download.convert()
    return file_path


# All manipulations with files are made in this function.
def pre_download(update: Update, message: str) -> tuple[bool, str]:
    check = check_url(message)
    if not check[0]:
        return check
    result = run_all(check[1], str(update.effective_chat.id))
    if not result[0]:
        return result
    return (True, result[1])


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    commands_handler = CommandHandler('commands', commands)
    info_handler = CommandHandler('info', info)
    love = CommandHandler('iloveyou', iloveyou)
    meme = CommandHandler('meme', random_meme)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(message_handler)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(commands_handler)
    application.add_handler(info_handler)
    application.add_handler(love)
    application.add_handler(meme)
    application.add_handler(unknown_handler)
    application.add_error_handler(error)

    application.run_polling()


if __name__ == '__main__':
    main()
