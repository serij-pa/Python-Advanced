import unittest

from module_03_ci_culture_beginning.homework.hw3.accounting import app, storage

class TestAccounting(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.add_url = "/add/"
        self.calculate_url = "/calculate/"
        self.storage = storage
        self.test_year = "2024"
        self.mistake_year = "2023"
        self.test_month = "12"
        self.mistake_month = "11"

    def test_add_1(self):
        test_expenses_period = "Неверно введена дата"
        test_expenses_for_period = f"{self.test_year}/1500"
        response = self.app.get(self.add_url + test_expenses_for_period)
        response_text = response.data.decode()
        self.assertEqual(test_expenses_period, response_text)

    def test_add_2(self):
        test_expenses_period = "Траты {2024: {'total': 1500, 12: 1500}}"
        test_expenses_for_period = "20241212/1500"
        response = self.app.get(self.add_url + test_expenses_for_period)
        response_text = response.data.decode()
        self.assertEqual(test_expenses_period, response_text)

    def test_calculate_year_1(self):
        response = self.app.get(self.calculate_url + self.test_year)
        response_text = response.data.decode()
        test_response = f"За {self.test_year} год было потрачено {self.storage[int(self.test_year)]["total"]}"
        self.assertEqual(test_response, response_text)

    def test_calculate_year_2(self):
        test_response = f"Трат за {self.mistake_year} год не было"
        response = self.app.get(self.calculate_url + self.mistake_year)
        response_text = response.data.decode()
        self.assertEqual(test_response, response_text)

    def test_calculate_month_1(self):
        test_request = f"За {self.test_month}.{self.test_year}г. было потрачено {self.storage[int(self.test_year)]["total"]}"
        response = self.app.get(self.calculate_url + self.test_year + "/" + self.test_month)
        response_text = response.data.decode()
        self.assertEqual(test_request, response_text)

    def test_calculate_month_2(self):
        request = f"Трат за {self.mistake_month}.{self.mistake_year}г. не было"
        response = self.app.get(self.calculate_url + self.mistake_year + "/" + self.mistake_month)
        response_text = response.data.decode()
        self.assertEqual(request, response_text)

    def tearDown(self):
        print("тест окончен")
