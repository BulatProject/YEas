import unittest
from .. import URLS, EXAMPLES, CLEAN_LINK, ERRORS, Checker
import requests

STREAM = '<Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus" progressive="False" type="audio">'

class TestChecker(unittest.TestCase):
    def test_check_status_code(self):
        urls = ['https://youtu.be/7PCkvCPvDXk', 
                'https://youtu.be/1oMgxa32A7g', 
                'https://www.youtube.com/watch?v=7-x3uD5z1bQ&list=PLZ1oGv-Tyew2v3zjJNX5E1PxU3WPFKbmM&index=23&ab_channel=HarryStylesVEVO', 
                'https://www.youtube.com/watch?v=DRHTr6wl3Q4&ab_channel=DoraSalvatore', 
                'https://www.youtube.com/watch?v=DRHTr6wl3Q4',
                'https://bad.link']
        expected_outputs = [STREAM,
                            STREAM, 
                            STREAM,
                            STREAM,
                            STREAM, 
                            f"Ссылка не соответстует требованиям:\n{CLEAN_LINK}"]
        for i, url in enumerate(urls):
            test = Checker(url)
            result = test.check_status_code()
            self.assertEqual(result, expected_outputs[i])

if __name__ == '__main__':
    unittest.main()
