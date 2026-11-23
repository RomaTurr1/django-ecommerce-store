from django.contrib import admin
from .models import Category, Product

# admin.site.register(Category)
# admin.site.register(Product)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = { 'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'description', 'image']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name', 'price', 'category']
    list_editable = ['name', 'price']

