from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'phone_number', 'delivery_method', 'status']
    list_filter = ['delivery_method', 'status']
    search_fields = ['user_name', 'phone_number']
    list_editable = ['status']
    inlines = [OrderItemInline]

admin.site.register(OrderItem)
