from django import forms

from .models import Offer, Request


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('title', 'offer_description')


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = {'title', 'service_type', 'price', 'start_date', 'deadline', 'request_description', 'image'}
