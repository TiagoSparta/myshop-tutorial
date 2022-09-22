from apps.cart.cart import Cart
from django.shortcuts import render

from .forms import OrderCreateForm
from .models import OrderItem
from django.db import connection


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            
            # Usando bulk_create
            items_list = []            
            for item in cart:
                order_item = OrderItem(order=order,
                                       product=item['product'],
                                       price=item['price'],
                                       quantity=item['quantity'])
                items_list.append(order_item)
            OrderItem.objects.bulk_create(items_list)
           
            # clear the cart
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
