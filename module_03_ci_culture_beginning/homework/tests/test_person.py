import unittest
from module_03_ci_culture_beginning.homework.hw4.person import Person

class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person("vanja", 2014, "Moskau")
        self.test_age = 42
        self.test_name = "vitja"
        self.test_address = "Piter"

    def test_get_age(self):
        self.assertNotEqual(self.test_age, self.person.get_age())

    def test_get_name(self):
        self.assertEqual(self.person.name, self.person.get_name())

    def test_set_name(self):
        test_name1 = self.person.name
        self.person.set_name(self.test_name)
        test_name2 = self.person.name
        self.assertNotEqual(test_name1, test_name2)

    def test_set_address(self):
        test_address1 = self.person.address
        self.person.set_address(self.test_address)
        test_address2 = self.person.address
        self.assertNotEqual(test_address1, test_address2)

    def test_get_address(self):
        self.assertEqual(self.person.address, self.person.get_address())

