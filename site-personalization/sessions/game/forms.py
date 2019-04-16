from django import forms
from .models import PlayerGameInfo

class AnswerForm(forms.ModelForm):
    answer = forms.CharField(label='Ответ')

    class Meta(object):
        model = PlayerGameInfo
        # fields = ('answer',)
        exclude = ('id',)
