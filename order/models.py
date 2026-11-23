from django.db import models
from main.models import Product

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('delivery', 'Доставка'),
    ]

    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Завершён'),
    ]

    user_name = models.CharField(max_length=50, verbose_name='Имя покупателя')
    phone_number = models.CharField(max_length=30, verbose_name='Телефон')
    address = models.CharField(max_length=100, blank=True, verbose_name='Адрес доставки')
    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES,
        default='pickup',
        verbose_name='Способ получения'
    )
    email = models.EmailField(blank=True, verbose_name='Электронная почта')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус заказа'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Заказ №{self.id} - {self.user_name}"
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}шт."
    
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
