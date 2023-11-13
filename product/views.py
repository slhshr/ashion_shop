from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
import datetime
import json

from .forms import *
from .models import *
# Create your views here.


def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(
            Q(category__name__icontains=q) |
            Q(title__icontains=q))
    if products:
        context = {'products': products}
        return render(request, 'product/search.html', context)
    else:
        messages.warning(request, 'The product was not found!')

    return render(request, 'product/search.html')


def shop(request):
    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.filter(user=user).first()
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.cart_item

    else:
        items = []
        order = {'cart_item': 0, 'cart_total': 0}
        cartItems = order['cart_item']

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    products = Product.objects.filter(
        Q(category__name__icontains=q) |
        Q(title__icontains=q))
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories, 'cartItems': cartItems, 'items': items}

    return render(request, 'product/shop_list.html', context)


def category(request, id):
    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.filter(user=user).first()
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.cart_item

    else:
        items = []
        order = {'cart_item': 0, 'cart_total': 0}
        cartItems = order['cart_item']

    products = Product.objects.filter(category_id=id)
    categories = Category.objects.all()

    context = {'products': products, 'categories': categories, 'cartItems': cartItems, 'items': items}

    return render(request, 'product/category.html', context)


def customer_profile(request):
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    print(customer, 'here', user)
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            customer.save()
            messages.success(request,f'Dear "{customer.user.username}", your customer information was updated successfully!')
            return redirect('product:customer_profile')
        for error in list(form.errors.values()):
            messages.error(request, error)

    print(customer, 'there')
    form = CreateCustomerForm(instance=customer)
    categories = Category.objects.all()
    context = {'form': form, 'categories': categories}
    return render(request, 'product/new_customer.html', context)


def product_details(request, pk):
    categories = Category.objects.all()
    product = Product.objects.get(id=pk)
    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.filter(user=user).first()
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.cart_item

    else:
        items = []
        order = {'cart_item': 0, 'cart_total': 0, 'shipping': False}
        cartItems = order['cart_item']
    context = {'product': product, 'categories': categories, 'items': items, 'cartItems': cartItems}
    return render(request, 'product/details.html', context)


# @login_required(login_url='/accounts/login')
def delete_product(request, pk):
    categories = Category.objects.all()
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        messages.info(request, 'The product was deleted!')
        return redirect('index')

    return render(request, 'product/delete_form.html', {'obj': product.title, 'categories': categories})


# @login_required(login_url='/accounts/login')
def new_product(request):
    categories = Category.objects.all()
    page = 'new_product'
    form = ProductForm()

    if request.method == 'POST':
        print(request.POST)
        form = ProductForm(request.POST)
        print(form)
        if form.is_valid():
            print('np')
            f = form.save()
            messages.success(request, f'"{f.title}" was created successfully.')
            return redirect('index')
        for error in list(form.errors.values()):
            messages.error(request, error)

    context = {'form': form, 'page': page, 'categories': categories}
    return render(request, 'product/product_cu_form.html', context)


@login_required(login_url='/accounts/login')
def update_product(request, pk):
    categories = Category.objects.all()
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            f = form.save()
            messages.success(request, f'"{f.title}" was updated successfully.')
            return redirect('index')
    context = {'form': form, 'categories': categories}
    return render(request, 'product/product_cu_form.html', context)


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        categories = Category.objects.all()
        print(user, 'cart')
        # if Customer.objects.filter(user=user).exists():
        print('here cart')
        customer, created = Customer.objects.get_or_create(user=user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        print(items, 'cart')
        cartItems = order.cart_item

        # else:
        #     messages.info(request, f'Dear "{user.username}", add your customer information please!')
        #     print('there cart')
        #     return redirect('product:new_customer')

    else:
        categories = Category.objects.all()
        items = []
        order = {'cart_item': 0, 'cart_total':0, 'shipping': False}
        cartItems = order['cart_item']
    context = {'categories': categories, 'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'product/cart.html', context)


def checkout(request):
    page = 'checkout'
    if request.user.is_authenticated:
        user = request.user
        categories = Category.objects.all()
        customer = Customer.objects.filter(user=user).first()
        order = Order.objects.filter(customer=customer, complete=False).first()
        items = order.orderitem_set.all()
        cartItems = order.cart_item

        if ShippingAddress.objects.filter(customer=customer).exists():
            try:
                shipping = ShippingAddress.objects.get(customer=customer)
                # shipping = ShippingAddress.objects.filter(customer=customer).first()
                if customer.full_name == '' and shipping.address == '':
                    print('here, address')
                    messages.info(request, f'Dear "{user.username}", add your shipping address please.')
                    return redirect('product:shipping_address')

                else:
                    print('there, address', shipping.address)
                    context = {'items': items, 'order': order, 'cartItems': cartItems, 'page': page, 'user': user,
                               'shipping': shipping, 'customer': customer,'categories': categories}
                    return render(request, 'product/checkout.html', context)
            except:
                messages.info(request, f'Dear "{user.username}", add your shipping address please.')
                return redirect('product:shipping_address')

    else:
        categories = Category.objects.all()
        user = []
        customer = []
        items = []
        order = {'cart_item': 0, 'cart_total': 0}
        cartItems = order['cart_item']
    context = {'categories': categories, 'items': items, 'order': order, 'cartItems': cartItems, 'page': page, 'user': user, 'customer': customer}
    return render(request, 'product/checkout.html', context)


def shipping_address(request):
    if request.user.is_authenticated:
        print('before sh post')
        if request.method == 'POST':
            user = request.user
            customer, created = Customer.objects.get_or_create(user=user)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            print('after sh post', customer.user.username)
            name = request.POST.get('full_name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            state = request.POST.get('state')
            city = request.POST.get('city')
            zipcode = request.POST.get('zipcode')
            if name and phone and address and state and city and zipcode:
                print('ship valid')
                customer.full_name = name
                customer.phone = phone
                customer.save()

                shipping = ShippingAddress()
                shipping.customer = customer
                shipping.order = order
                shipping.address = address
                shipping.state = state
                shipping.city = city
                shipping.zipcode = zipcode
                shipping.save()
                messages.success(request, f'Dear "{user.username}", your shipping address was added successfully!')
                return redirect('product:checkout')

        categories = Category.objects.all()
        user = request.user
        customer = Customer.objects.filter(user=user).first()
        order = Order.objects.filter(customer=customer, complete=False).first()
        cartItems = order.cart_item
        context = {'customer': customer, 'order': order, 'categories': categories, 'cartItems': cartItems}
        return render(request, 'product/shipping.html', context)

    return redirect('account:login')


def update_cart(request):
    print(request.body)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId, action)

    user = request.user
    customer = Customer.objects.filter(user=user).first()
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def order_status(request):
    print('data: ', request.body)

    return JsonResponse('payment completed', safe=False)


def order_factor(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        transaction_id = datetime.datetime.now().timestamp()
        user = request.user
        customer = Customer.objects.filter(user=user).first()
        order = Order.objects.filter(customer=customer, complete=False).first()
        order.transaction_id = transaction_id
        order.complete = True
        print(order.complete)
        order.save()
        messages.success(request, 'Thanks for your shopping!')
    else:
        categories = Category.objects.all()
        transaction_id = []
        order = []
        customer = []
    context = {'transaction_id': transaction_id, 'order': order, 'customer': customer, 'categories': categories}
    return render(request, 'product/factor.html', context)




