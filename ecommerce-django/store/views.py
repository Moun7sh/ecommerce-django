from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import Product, Order, OrderItem
from .forms import SignUpForm
from django import forms

#Fetch the data from the model and send it to the template
#Handle Cart 
#Handle Checkout
#Handle Sign up

# --------------------------------
# PRODUCT LIST & DETAIL
# --------------------------------


def product_list(request):
    products = Product.objects.all()  # fetch all product from database
    return render(request, 'store/product_list.html', {'products': products})

#Fetch one product details using slug if product not fount show 404 error

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})
# --------------------------------
# CART SYSTEM
# --------------------------------

# Create cart inside the session I will act like temporary storage

def _get_cart(request):
    return request.session.setdefault('cart', {})

def add_to_cart(request, product_id):
    cart = _get_cart(request)
    qty = int(request.POST.get('quantity', 1)) #Check the quantity
    cart[str(product_id)] = cart.get(str(product_id), 0) + qty #Add product to cart
    request.session.modified = True #Save the Cart
    return redirect('store:cart') # The user is sent to the Cart page

def view_cart(request):
    cart = _get_cart(request)
    items = []
    total = 0

    for pid, qty in cart.items():
        product = Product.objects.get(pk=pid)
        items.append({
            'product': product,
            'quantity': qty,
            'subtotal': product.price * qty
        })
        total += product.price * qty

    return render(request, 'store/cart.html', {'items': items, 'total': total}) #Show to the html page


# --------------------------------
# CHECKOUT FORM
# --------------------------------

class CheckoutForm(forms.Form):  #Check the user input valid
    full_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)

# --------------------------------
# CHECKOUT VIEW
# --------------------------------
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect('store:product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid(): # Create a new Order entry in database
            order = Order.objects.create(
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                user=request.user if request.user.is_authenticated else None,
                paid=False
            )
            #Create OrderItem for each product in cart
            for pid, qty in cart.items():
                product = Product.objects.get(pk=pid)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=product.price
                )
            request.session['cart'] = {}
            messages.success(request, "Order placed successfully!")
            return redirect('store:product_list')
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {'form': form})

# --------------------------------
# SIGNUP VIEW
# --------------------------------
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Create a form object
        if form.is_valid():
            user = form.save(commit=False) # Save as temporarly
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('store:product_list')
    else:
        form = SignUpForm()

    return render(request, 'store/signup.html', {'form': form})
