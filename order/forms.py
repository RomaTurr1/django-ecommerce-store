from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user_name', 'phone_number', 'delivery_method', 'address', 'email', 'comment']
        labels = {
            'user_name': 'Имя покупателя',
            'phone_number': 'Номер телефона',
            'delivery_method': 'Способ получения',
            'address': 'Адрес доставки',
            'email': 'Электронная почта',
            'comment': 'Комментарий к заказу',
        }
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ваше имя'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+7 (___) ___-__-__'}),
            'delivery_method': forms.Select(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Адрес доставки (если доставка)'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'example@mail.ru'}),
            'comment': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Ваш комментарий к заказу...'}),
        }
