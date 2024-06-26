from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name
class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    company_category = models.CharField(max_length=50, null=True)
    slug = models.SlugField(max_length=50, unique=True)
    def __str__(self):
        return self.company_category

class Product(models.Model):
    nameProduct = models.CharField(max_length=50, null=True)
    price = models.FloatField()
    category = models.ManyToManyField(Category, related_name="product")
    image = models.ImageField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nameProduct
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url

class CustomerOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    def get_bill(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(CustomerOrder, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price  * self.quantity
        return total
        
class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(CustomerOrder, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=50,null=True)
    city = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50,null=True)
    mobile = models.CharField(max_length=50,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address






