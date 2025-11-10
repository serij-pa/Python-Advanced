"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app


class TestRegistrations(unittest.TestCase):
    @classmethod
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.base_url = '/registration'

    def test_register(self):
        data = {"email": "test@test.ru"}

        response = self.app.post(self.base_url,
                                 data = {
                                     "email": "test@test.ru",
                                     "phone" : 9991112233,
                                     "name" : "Testov Test",
                                     "address" : "ul Adressovaya",
                                     "index" : 107223,
                                     "comment" : "K chayu vosmi"})
        response_text = response.data.decode()
        print(response_text)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
