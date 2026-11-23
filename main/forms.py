from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'rating', 'text']
        labels = {
            'author': 'Ваше имя',
            'rating': 'Оценка',
            'text': 'Текст отзыва',
        }
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите ваше имя'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-input'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Напишите ваш отзыв...'
            }),
        }
