from pytube import Playlist


COMMA_MESSAGE_ERROR = 'Нет запятой - диапазон не распознан.'
HYPHEN = 'Нет дефиса - диапазон не распознан.'
SYMBOLS_ERROR = 'В диапазоне есть лишние символы - диапазон не распознан.'
RANGE_ERROR = 'В указанном диапазоне {} песен. Это больше 20.'

class Preparator:
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
        for i in range(len(playlist_range)):
            if not playlist_range[i].strip().isnumeric():
                return (False, SYMBOLS_ERROR)
            playlist_range[i] = int(playlist_range[i].strip())
        return (True, playlist_range)

    # Проверяет, сколько в диапазоне элементов.
    def check_range(self, playlist_range):
        if (playlist_range[1] - playlist_range[0]) < 21:
            return (True, playlist_range)
        return (False, RANGE_ERROR.format(playlist_range[1] - playlist_range[0]))

    # Превращаем ссылку на плейлист в список ссылок на композиции.
    def get_playlist(self, url):
        return Playlist(url).video_urls

