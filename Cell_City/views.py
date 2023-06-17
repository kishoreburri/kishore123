from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import Brand, Product, CartItem, Wishlist, Order, Address
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, FeedbackForm, AddressForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def home(request):
    mobile_brands = Brand.objects.all() 
    context = {
        'mobile_brands': mobile_brands
    }
    return render(request, 'home.html', context)

def products(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    products = Product.objects.filter(brand=brand)
    context = {
        'products': products,
        'brand': brand,
    }
    return render(request, 'products.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)

@login_required
def increase_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    if cart_item.quantity < cart_item.product.stock_quantity:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    elif cart_item.quantity <= 1:
        cart_item.delete()
    return redirect('cart')

@login_required
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity =+ 1
            cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.all()
    total_cost = 0
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        total_cost += item.subtotal

    context = {
        'cart_items': cart_items,
        'total_cost': total_cost
    }
    return render(request, 'cart.html', context)

@login_required
def wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(product_id)
        return redirect('wishlist')
    else:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        context = {'wishlist': wishlist}
        return render(request, 'wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(product)
        wishlist.save()
        return redirect('wishlist')
    else:
        return HttpResponse("Please login to add items to your wishlist.")

@login_required
def remove_from_wishlist(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=product_id)
        wishlist = Wishlist.objects.get(user=request.user)
        wishlist.products.remove(product)
    return redirect('wishlist')

from django.contrib.auth.decorators import login_required
from .forms import AddressForm


from django.contrib.auth.decorators import login_required
from .forms import AddressForm

@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    total_cost = 0
    for item in cart_items:
        total_cost += item.product.price * item.quantity

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = user
            address.save()
            order = Order.objects.create(user=user, address=address, price=total_cost, total_cost=total_cost)
            cart_items.delete()
            return redirect('payment_mode', order_id=order.id)
    else:
        form = AddressForm()

    return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items, 'total_cost': total_cost})




@login_required
def payment_mode(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        selected_payment_mode = request.POST.get('payment_mode')
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'payment_mode.html')

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

def view_invoice(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'invoice.html', {'order': order})

def contact(request):
    return render(request, 'contact.html')

def search_results(request):
    query = request.GET.get('query')
    results = Product.objects.filter(name__icontains=query)
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search_results.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def my_orders(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        if order.user == request.user and not order.is_cancelled:
            order.is_cancelled = True
            order.save()
            messages.success(request, 'Order cancelled successfully.')

    orders = Order.objects.filter(user=request.user)
    return render(request, 'my_orders.html', {'orders': orders})

from django.contrib.auth.forms import UserChangeForm

@login_required
def profile(request):
    saved = False
    max_addresses_reached = False

    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        address_form = AddressForm(request.POST)

        if form.is_valid() and address_form.is_valid():
            form.save()
            if Address.objects.filter(customer=request.user).count() < 3:
                address = address_form.save(commit=False)
                address.customer = request.user
                address.save()
                saved = True
            else:
                max_addresses_reached = True
    else:
        form = UserChangeForm(instance=request.user)
        address_form = AddressForm()

    addresses = Address.objects.filter(customer=request.user)

    return render(request, 'profile.html', {'user': request.user, 'form': form, 'address_form': address_form, 'saved': saved, 'addresses': addresses, 'max_addresses_reached': max_addresses_reached})

def edit_address(request, address_id):
    address = Address.objects.get(id=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'edit_address.html', {'form': form, 'address': address})

def delete_address(request, address_id):
    address = Address.objects.get(id=address_id)
    address.delete()
    return redirect('profile')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})




def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback.html', {'form': form})


def thank_you(request):
    return render(request, 'thank_you.html')

