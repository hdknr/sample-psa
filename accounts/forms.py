# coding: utf-8
from django import forms


class AuthConfirmForm(forms.Form):
    agreed = forms.BooleanField(required=True, label='Aggree to Login')
