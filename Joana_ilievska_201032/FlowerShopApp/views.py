from datetime import date

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Flower, Order, PaidOrder
from .forms import OrderForm
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    return render(request, "index.html")


def products(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            flower_id = request.POST.get('product_id')
            flower = Flower.objects.get(id=flower_id)
            order = Order(user=request.user, flower=flower)
            order.save()
            return redirect('products')
    qs = Flower.objects.all()
    context = {"products": qs, "form": OrderForm}
    return render(request, "products.html", context)


def basket(request):
    orders = Order.objects.filter(user=request.user)
    total_price = 0

    for order in orders:
        total_price += order.flower.price

    with_shipping = total_price + 150
    context = {
        'orders': orders,
        'total_price': total_price,
        'with_shipping': with_shipping,
    }

    return render(request, 'basket.html', context)


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('basket')


def customer_registration_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            error_message = 'Username is already taken. Please choose a different username.'
            return render(request, 'registration.html', {'error_message': error_message})

        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')

    return render(request, 'registration.html')


def customer_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')



def ordered(request):
    orders = Order.objects.filter(user=request.user)

    for order in orders:
        paidOrder = PaidOrder(user=request.user, flower=order.flower, date=date.today())
        order.delete()
        paidOrder.save()

    return render(request, 'thankyou.html', )


def notavailable(request):
    return render(request, 'Notavailable.html')

def AboutUs(request):
    return render(request, 'AboutUs.html')