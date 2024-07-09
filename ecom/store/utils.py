import json
from .models import *

def cookieCart(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = OrderItem.objects.all()
		cartItems = order.get_cart_items
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}

		print('cart:', cart)
		items = []
		order = {'get_cart_total':0,  'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
		try:

			for i in cart:
				cartItems += cart[i]["quantity"]

				product = Product.objects.get(id=i)
				total = (product.price * cart[i]["quantity"])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]["quantity"]


				item = {
					'product':{
						'id': product.id,
						'name': product.name,
						'price' : product.price,
						'imageURL' : product.imageURL,
						},
					'quantity': cart[i]["quantity"],
					'get_total': total
					}								
		except:
			pass

	return{'items':items, 'order':order, 'cartItems': cartItems}

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(user=user, complete=False)
		items = OrderItem.objects.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order'] 
		items = cookieData['items']  

		return {'items':items, 'order':order, 'cartItems': cartItems}



