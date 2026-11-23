from django.db import models

class Category(models.Model):
    NAME_CHOICES = [
        ("default", "Прочее"),
        ("clothes", "Одежда"),
        ("gadzhety", "Гаджеты")
    ]
    name = models.CharField(max_length=100, db_index=True, choices=NAME_CHOICES, default="default")
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='products/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self):
        return self.name