import requests
from pytube import YouTube

EXAMPLES = ['https://youtu.be/', 'youtu.be/', 'https://www.youtube.com/watch?', 'youtube.com/watch?', 'https://youtube.com/playlist?', 'youtube.com/playlist?']
CLEAN_LINK = f'Ссылка на видео должна начинаться как один из примеров и быть не длиннее 130 символов:\n"{EXAMPLES[0]}"\n"{EXAMPLES[1]}"\n"{EXAMPLES[2]}"\n"{EXAMPLES[3]}"\n"{EXAMPLES[4]}"\n"{EXAMPLES[5]}"'
ERRORS = ["Ресурс недоступен.", 
            r'Ошибка в ссылке или доступ к видео ограничен. Видео: {} Код ошибки: {}.',
            f"Ссылка не соответстует требованиям:\n{CLEAN_LINK}",
            "Доступ к видео ограничен, или по ссылке видео нет."]

class Checker:
    def __init__(self, url):
        fine_link = (len(url) < 131) and (url.startswith(EXAMPLES[0]) or url.startswith(EXAMPLES[1]) or url.startswith(EXAMPLES[2]) or url.startswith(EXAMPLES[3]) or url.startswith(EXAMPLES[4]) or url.startswith(EXAMPLES[5]))
        if fine_link:
            self.base_check = (True, url)
        else:
            self.base_check = (False, ERRORS[2])

    def check_status_code(self, url):
        try:
            response = requests.get(url)
        except:
            return (False, ERRORS[0])
        if response.status_code != 200:
            return (False, ERRORS[1].format(self.url, response.status_code))
        return (True, url)

    def check_access(self, url):
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).last()
        except:
            return (False, ERRORS[3])
        return (True, yt)
