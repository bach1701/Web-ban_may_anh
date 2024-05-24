from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
import json

# Create your views here.
def home(request):
    categories = Category.objects.filter(is_sub = False)
    products = Product.objects.all()
    context={'categories':categories,'products' : products}
    return render(request, 'app/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = CustomerOrder.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items' : 0,'order.get_bill' : 0}
    context={'items' : items, 'order' : order}
    return render(request, 'app/cart.html',context)



def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = CustomerOrder.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items' : 0,'order.get_bill' : 0}
    context={'items' : items, 'order' : order}
    return render(request, 'app/checkout.html',context)

def updateItem(request):
    
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = CustomerOrder.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added',safe=False)

def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context={'categories': categories,'products' : products, 'active_category' : active_category}
    return render(request, 'app/category.html',context)

def detail(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = CustomerOrder.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items' : 0,'order.get_bill' : 0}
        
    categories = Category.objects.filter(is_sub = False)
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    context={'products' : products, 'categories': categories,'items' : items, 'order' : order}
    return render(request, 'app/detail.html',context)



