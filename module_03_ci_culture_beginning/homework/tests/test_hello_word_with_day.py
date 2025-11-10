import unittest
from datetime import datetime

from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app

test_weekdays_tuple = ("Хорошего понедельника",
                       "Хорошего вторника",
                       "Хорошей среды",
                       "Хорошего четверга",
                       "Хорошей пятницы",
                       "Хорошей субботы",
                       "Хорошего воскресенья")


class TestHelloWord(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_check_day_of_week(self):
        username = "NoName"
        current_day = test_weekdays_tuple[datetime.today().weekday()]
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        print(current_day, response_text, response)
        self.assertTrue(current_day in response_text)
