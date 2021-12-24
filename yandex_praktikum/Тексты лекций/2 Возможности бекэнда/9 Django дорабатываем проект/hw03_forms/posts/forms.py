from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text')

    def clean_text(self):
        text = self.cleaned_data['text']

        if len(text) == 0:
            raise forms.ValidationError(
                'Это поле не должно быть пустым!', params={'text': text},
            )

        return text
