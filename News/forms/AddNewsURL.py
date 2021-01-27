from News.models.NewsURL import NewsURL
from django import forms

class AddNewsURL(forms.ModelForm):
    class Meta:
        model = NewsURL
        fields = ('news',)