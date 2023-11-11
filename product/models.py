from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


phone_validator = RegexValidator(r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$", "The phone number provided is invalid")
# Create your models here.


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=11, validators=[phone_validator], unique=True, null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    product_image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.product_image.url
        except:
            url = ''
        return url


class Order(models.Model):
    # Status = [
    #     ('purchased', 'purchased'),
    #     ('failed', 'failed'),
    #     ('waiting', 'waiting'),
    # ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)
    # status = models.CharField(choices=Status, max_length=20, default='purchased')

    def __str__(self):
        return str(self.id)

    @property
    def cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.total for item in orderitems])
        return total

    @property
    def cart_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        total = self.quantity * self.product.price
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
