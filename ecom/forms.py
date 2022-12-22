from django import forms
# from django.contrib.auth.models import User
from . import models
from django.db.models import TextField, Model


class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['name','feedback']
        form_feedback = TextField()


class MerchantForm(forms.ModelForm):
    class Meta:
        model=models.Merchant
        fields=['MID',]
        form_merchant = TextField()