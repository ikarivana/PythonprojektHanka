from django.test import TestCase
from django.core.exceptions import ValidationError
from viewer.models import Pedikura


class PedikuraModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Vytvoření testovacích dat před spuštěním testů
        cls.pedikura = Pedikura.objects.create(
            name='Pedikura moje',
            procedure_time=10,
            description='Pedikura moje description',
            price=1000
        )

    def setUp(self):
        # Tento setUp se spouští před každým testem
        self.pedikura = Pedikura.objects.get(name='Pedikura moje')

    def test_create_pedikura(self):
        # Test vytvoření nové pedikúry
        self.assertEqual(self.pedikura.name, 'Pedikura moje')
        self.assertEqual(self.pedikura.procedure_time, 10)
        self.assertEqual(self.pedikura.description, 'Pedikura moje description')

        self.assertEqual(self.pedikura.price, 1000)


    def test_name_max_length(self):
        # Test maximální délky názvu
        self.pedikura.name = 'x' * 31  # Překročení max_length=30
        with self.assertRaises(ValidationError):
            self.pedikura.full_clean()

    def test_unique_name(self):
        # Test unikátnosti názvu
        duplicate_pedikura = Pedikura(
            name='Pedikura moje',
            procedure_time=20,
            price=2000
        )
        with self.assertRaises(ValidationError):
            duplicate_pedikura.full_clean()

    def test_blank_values(self):
        # Test povinných polí
        invalid_pedikura = Pedikura(
            name='',
            procedure_time=None,
            price=None
        )
        with self.assertRaises(ValidationError):
            invalid_pedikura.full_clean()

    def test_string_representation(self):
        # Test __str__ metody
        self.assertEqual(str(self.pedikura), 'Pedikura moje')

    def test_repr_representation(self):
        # Test __repr__ metody
        expected = "Pedikura(name=Pedikura moje procedure_time=10 description=Pedikura moje description price=1000)"
        self.assertEqual(repr(self.pedikura), expected)

    def test_ordering(self):
        # Test řazení podle jména
        Pedikura.objects.create(name='Pedikura jindra', procedure_time=15, price=1200)
        Pedikura.objects.create(name='Pedikura gab', procedure_time=20, price=1500)
        pedikury = Pedikura.objects.all()
        self.assertEqual(pedikury[0].name, 'Pedikura gab')
        self.assertEqual(pedikury[1].name, 'Pedikura jindra')
        self.assertEqual(pedikury[2].name, 'Pedikura moje')


