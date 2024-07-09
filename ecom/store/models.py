from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True ,blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Catalog(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=150)
	publisher = models.CharField(max_length=300)
	description = models.TextField()
	pub_date = models.DateTimeField(default=datetime.now()) 

	def __str__(self):
		return self.name

class Order(models.Model):
	customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True)	
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=True)
	transaction_id = models.CharField(max_length=200, null=True)

	def __str__(self):
		return str(self.id)

	@property	
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property	
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total


class OrderItem(models.Model):
	product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True,null=True)
	quantity = models.IntegerField(default=0, null=True,blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total


class Cart(models.Model):
	user = models.OneToOneField('Customer', on_delete=models.CASCADE)
	products = models.ManyToManyField('Product')

class Product(models.Model):
	category = models.ForeignKey('CatalogCategory', related_name='product', on_delete= models.CASCADE)
	name = models.CharField(max_length=300)
	slug = models.SlugField(max_length=150)
	description = models.TextField()
	photo = models.ImageField(upload_to='product_photo', blank=True)
	manufacturer = models.CharField(max_length=300, blank=True)
	price = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url= self.photo.url
		except:
			url= ''
		return url
	

class CatalogCategory(models.Model):
	catalog = models.ForeignKey('Catalog', related_name= 'categories', on_delete= models.CASCADE)
	parent = models.ForeignKey('self', blank=True, null = True,  related_name='children', on_delete=models.CASCADE)
	name = models.CharField(max_length=300)
	slug = models.SlugField(max_length=150)
	description = models.TextField(blank=True)

	def __str__(self):
		if self.parent:
			return '%s: %s - %s' % (self.catalog.name, self.parent.name, self.name)
		return '%s: %s' % (self.catalog.name, self.name)
		
class ProductDetail(models.Model):
	product = models.ForeignKey('Product', related_name = 'details', on_delete=models.CASCADE)
	attribute = models.ForeignKey('ProductAttribute', on_delete=models.CASCADE)
	value = models.CharField(max_length=500)
	description = models.TextField(blank=True)

	def __str__(self):
		return '%s: %s - %s' % (self.product, self.attribute, self.value)


class ProductAttribute(models.Model):
	name = models.CharField(max_length=300)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name






	
	 
	 

	
 
 
 


