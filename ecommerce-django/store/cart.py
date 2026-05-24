from django.shortcuts import redirect, render
from store.models import Product


def _get_cart(request):
    return request.session.setdefault('cart', {})

def add_to_cart(request, product_id):
    cart = _get_cart(request)
    qty = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    cart[str(product_id)] = cart.get(str(product_id), 0) + qty
    request.session.modified = True
    return redirect('store:cart')

def view_cart(request):
    cart = _get_cart(request)
    items = []
    total = 0
    for pid, qty in cart.items():
        product = Product.objects.get(pk=pid)
        items.append({'product': product, 'quantity': qty, 'subtotal': product.price * qty})
        total += product.price * qty
    return render(request, 'store/cart.html', {'items': items, 'total': total})
