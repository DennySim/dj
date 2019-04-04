from django import forms
from .models import Review, Car
from ckeditor.widgets import CKEditorWidget


class CarAdminForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = ['brand', 'model']


class ReviewAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Review
        fields = ['car', 'title', 'text']
