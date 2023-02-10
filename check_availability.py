import requests
from pytube import YouTube

EXAMPLES = ['https://youtu.be/', 'https://www.youtube.com/watch?', 'youtu.be/', 'youtube.com/watch?']
CLEAN_LINK = f'Ссылка на видео должна начинаться как один из примеров:\n"{EXAMPLES[0]}"\n"{EXAMPLES[1]}"\n"{EXAMPLES[2]}"\n"{EXAMPLES[3]}"'
ERRORS = ["Ресурс недоступен.", 
            r'Ошибка в ссылке или доступ к видео ограничен. Видео: {} Код ошибки: {}.',
            f"Ссылка не соответстует требованиям:\n{CLEAN_LINK}",
            "Video is restricted or private."]

class Checker:
    def __init__(self, url):
        fine_link = url.startswith(EXAMPLES[0]) or url.startswith(EXAMPLES[1]) or url.startswith(EXAMPLES[2]) or url.startswith(EXAMPLES[3])
        if fine_link:
            self.url = url
        else:
            self.url = False

    def check_status_code(self):
        if self.url:
            try:
                response = requests.get(self.url)
            except:
                return ERRORS[0]
            if response.status_code == 200:
                return self.check_access()
            else:
                return ERRORS[1].format(self.url, response.status_code)
        else:
            return ERRORS[2]

    def check_access(self):
        try:
            yt = YouTube(self.url)
            stream = yt.streams.filter(only_audio=True).last()
        except:
            return ERRORS[3]
        return yt
