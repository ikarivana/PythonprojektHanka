from django.test import TestCase

class ExampleTest(TestCase):

    @ classmethod
    def setUpTestData(cls):
        print("setUpTestData: Spusti se jednou a slouží k nastavení databáze")

    def setUp(self):
        print("setUp: Spustí se před každým testem")

    def test_false(self):
        result = False
        self.assertFalse(result)

    def test_add(self):
        print("Testovací metoda: test_add")
        result = 1 + 4
        self.assertEqual(result, 5)