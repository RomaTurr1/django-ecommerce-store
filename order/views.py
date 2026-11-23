from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from main.models import Product
from .forms import OrderForm


def create_order(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect('main')

    # Расчет состава корзины по существующей логике
    products = Product.objects.filter(id__in=cart.keys())
    if not products.exists():
        return redirect('main')

    items = []
    total_price = Decimal("0.00")
    total_quantity = 0

    for product in products:
        quantity = cart.get(str(product.id), 0)
        if quantity > 0:
            item_total = product.price * quantity
            items.append({
                "product": product,
                "quantity": quantity,
                "item_total": item_total
            })
            total_price += item_total
            total_quantity += quantity

    if not items or total_quantity <= 0:
        return redirect('main')

    error = ''
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity']
                )

            del request.session["cart"]
            request.session.modified = True

            return redirect('main')
        else:
            error = 'Пожалуйста, проверьте правильность заполнения полей.'
    else:
        form = OrderForm()

    context = {
        "form": form,
        "error": error,
        "items": items,
        "total_price": total_price,
        "total_quantity": total_quantity
    }

    return render(request, "order/create_order.html", context)
