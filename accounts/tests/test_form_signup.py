__author__ = 'yangjian'
__date__ = '2018/6/29 16:03'


from django.test import TestCase
from accounts.forms import SignUpForm

class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)