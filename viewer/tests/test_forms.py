import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loubnatural.settings')
import django
django.setup()

from django.test import TestCase
from django import forms
from django.contrib.auth.models import User

from viewer.forms import PedikuraReviewForm
from viewer.models import Pedikura, PedikuraReview


class PedikuraReviewFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # testování pedikura
        cls.pedikura = Pedikura.objects.create(
            name='Testovací pedikúra',
            procedure_time=30,
            price=500,
            description='Testovací popis'
        )
        # testování uživatele
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def setUp(self):
        self.form_data = {
            'rating': 3,
            'comment': 'Testovací komentář',
        }
        self.test_review = PedikuraReview.objects.create(
            pedikura=self.pedikura,
            user=self.user,
            rating=4,
            comment='Původní komentář'
        )

    def test_valid_form(self):
        """Test platného formuláře"""
        form = PedikuraReviewForm(data=self.form_data, instance=self.test_review)
        self.assertTrue(form.is_valid())

    def test_invalid_rating_too_low(self):
        """Test příliš nízkého hodnocení"""
        self.form_data['rating'] = 0
        form = PedikuraReviewForm(data=self.form_data, instance=self.test_review)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_invalid_rating_too_high(self):
        """Test příliš vysokého hodnocení"""
        self.form_data['rating'] = 6
        form = PedikuraReviewForm(data=self.form_data, instance=self.test_review)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_comment_optional(self):
        """Test že komentář je nepovinný"""
        self.form_data['comment'] = ''
        form = PedikuraReviewForm(data=self.form_data, instance=self.test_review)
        self.assertTrue(form.is_valid())

    def test_rating_required(self):
        """Test že hodnocení je povinné"""
        self.form_data.pop('rating')
        form = PedikuraReviewForm(data=self.form_data, instance=self.test_review)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_form_fields_labels(self):
        """Test správných popisků polí"""
        form = PedikuraReviewForm()
        self.assertEqual(form.fields['rating'].label, 'Hodnocení (1-5)')
        self.assertEqual(form.fields['comment'].label, 'Komentář')

    def test_form_widgets(self):
        """Test použitých widgetů"""
        form = PedikuraReviewForm()
        self.assertIsInstance(form.fields['rating'].widget, forms.NumberInput)
        self.assertIsInstance(form.fields['comment'].widget, forms.Textarea)

    def test_rating_widget_attributes(self):
        """Test atributů widgetu pro hodnocení"""
        form = PedikuraReviewForm()
        self.assertEqual(
            form.fields['rating'].widget.attrs['class'],
            'form-control'
        )

    def test_comment_widget_attributes(self):
        """Test atributů widgetu pro komentář"""
        form = PedikuraReviewForm()
        self.assertEqual(
            form.fields['comment'].widget.attrs['class'],
            'form-control'
        )
        self.assertEqual(
            form.fields['comment'].widget.attrs['rows'],
            3
        )

    def test_update_review(self):
        """Test aktualizace existující recenze"""
        self.form_data['rating'] = 5
        self.form_data['comment'] = 'Aktualizovaný komentář'

        form = PedikuraReviewForm(data=self.form_data, instance=self.test_review)
        self.assertTrue(form.is_valid())
        updated_review = form.save()

        # Ověření, že recenze byla správně aktualizována
        self.assertEqual(updated_review.rating, 5)
        self.assertEqual(updated_review.comment, 'Aktualizovaný komentář')
        self.assertEqual(updated_review.pedikura, self.pedikura)
        self.assertEqual(updated_review.user, self.user)



