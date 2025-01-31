from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Humster


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁёйцукенгшщзхъфывапролджэячсмитьбю01234567890- "
    code = "russian"

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел!"

    def __call__(self,value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)
class AddPostForm(forms.ModelForm):

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории", empty_label="Категория не выбрана")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label="Cупруг", empty_label="Не жената" )

    class Meta:
        model = Humster
        fields = ['title', 'slug', 'content','photo', 'is_published', 'cat', 'husband', 'tags',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = {'slug': 'URL', 'is_published':'Статус'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина строки превышает 50 символов!")

        return title

class UploadFileForm(forms.Form):
    file = forms.FileField(label='File')