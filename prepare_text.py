from pytube import Playlist
from TEXTS import COMMA_MESSAGE_ERROR, HYPHEN, SYMBOLS_ERROR, RANGE_ERROR, LENGHT_ERROR, INSTRUCTION_ERROR, STARTING_WORDS, NO_FIRST_NUM_ERROR


class Preparator:
    def __init__(self, text):
        self.results = self.starting_check(text)

    def starting_check(self, text):
        if text.lower().startswith('трек,') and (len(text)) > 5:
            return (True, STARTING_WORDS[0])
        if text.lower().startswith('лист,') and (len(text)) > 5:
            return (True, STARTING_WORDS[1])
        return (False, LENGHT_ERROR)

    # Делим сообщение на диапазон и url + проверяем диапазон на наличие букв.
    # Возвращает кортеж (True/False, имя ошибки/диапазон и url)
    def divide_n_clean_message(self, message):
        if ',' not in message:
            return (False, COMMA_MESSAGE_ERROR)
        playlist_range, url = message.split(',')
        url = url.strip()
        if '-' not in playlist_range:
            return (False, HYPHEN)
        playlist_range = playlist_range.split('-')
        correct_range = self.check_symbols(playlist_range)
        if not correct_range[0]:
            return correct_range
        return (True, correct_range[1], url)

    def check_symbols(self, playlist_range):
        if playlist_range[0] is None:
            return (False, NO_FIRST_NUM_ERROR)
        for i in range(2):
            if not playlist_range[i].strip().isnumeric():
                return (False, SYMBOLS_ERROR)
            playlist_range[i] = int(playlist_range[i].strip())
        playlist_range[0] -= 1
        return (True, playlist_range)

    def check_range(self, playlist_range):
        if -1 > (playlist_range[1] - playlist_range[0]) < 21:
            return (True, playlist_range)
        return (False, RANGE_ERROR.format(playlist_range[1] - playlist_range[0]))

    # Превращаем ссылку на плейлист в список ссылок на композиции.
    def get_playlist(self, url):
        return Playlist(url).video_urls