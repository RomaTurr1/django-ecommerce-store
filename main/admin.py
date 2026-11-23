from django.contrib import admin
from .models import Category, Product, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'description', 'image']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name', 'price', 'category']
    list_editable = ['name', 'price']
    inlines = [ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['author', 'text']
