from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from .utils import cookieCart, cartData
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.

def product_list_view(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = OrderItem.objects.all()
		cartItems = order.get_cart_items

	else:
		data = cartData(request)
		cartItems = data['cartItems']
	
	products = Product.objects.all()
	context = {'products':products, 'cartItems': cartItems}
	return render(request, 'base/index.html', context)


def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = OrderItem.objects.all()
		cartItems = order.get_cart_items


	else:
		data = cartData(request)
		cartItems = data['cartItems']
		order = data['order'] 
		items = data['items']  		
	context = {'items':items, 'order':order, 'cartItems': cartItems  }
	return render(request, 'base/cart.html', context)


def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = OrderItem.objects.all()
		cartItems = order.get_cart_items
	else:
		data= cartData(request)
		cartItems = data['cartItems']
		order = data['order'] 
		items = data['items']  


	context = {'items':items, 'order':order, 'cartItems': cartItems}
	return render(request, 'base/checkout.html', context)


def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = UserRegistrationForm()
	return render(request, 'registration/register.html', {'form':form})

def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			user= form.get_user()
			print("User authenticated successfully") 
			return redirect('products')
	else:
		form = UserRegistrationForm()
	return render(request, 'registration/login.html', {'form':form})



def updateItem(request):
	data = json.loads(request.body)
	productId = data['ProductId']
	action = data['action']
	print('action:', action)
	print('productId:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product )

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
	
	return JsonResponse('Item was added', safe=False)
			         
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    	
    else:
        # Assuming guestOrder is a function that handles guest checkout
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

   
    return JsonResponse({'success': True, 'message': 'Order processed'}, safe=False)


