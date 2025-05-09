from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import login  # ✅ 新增：用于注册后自动登录

from .models import Star, Order
from .forms import OrderForm, UserRegistrationForm  # ✅ 添加注册表单


def star_list(request):
    stars = Star.objects.all()
    confirmed_orders = Order.objects.filter(status='confirmed')
    confirmed_dict = {o.star_id: o for o in confirmed_orders}
    return render(request, 'catalog/star_list.html', {
        'stars': stars,
        'confirmed_orders': confirmed_dict
    })


def star_detail(request, pk):
    star = get_object_or_404(Star, pk=pk)
    confirmed_order = Order.objects.filter(star=star, status='confirmed').first()
    return render(request, 'catalog/star_detail.html', {
        'star': star,
        'confirmed_order': confirmed_order
    })


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.status = 'pending'
            order.price = 19.99
            order.save()
            messages.success(request, "Order created. Please proceed to payment.")
            return redirect('my_orders')
    else:
        form = OrderForm()
    return render(request, 'catalog/order_form.html', {'form': form})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'catalog/my_orders.html', {'orders': orders})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_orders(request):
    orders = Order.objects.all()
    return render(request, 'catalog/admin_orders.html', {'orders': orders})


@login_required
def pay_for_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status == 'pending':
        order.status = 'paid'
        order.save()
        messages.success(request, "Payment successful. Awaiting admin confirmation.")
    return redirect('my_orders')


@user_passes_test(lambda u: u.is_superuser)
def confirm_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.status == 'paid':
        order.status = 'confirmed'
        order.save()
        messages.success(request, f"Order '{order.name_given}' confirmed.")
    return redirect('admin_orders')


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    orders = Order.objects.all()
    stats = orders.values('star__constellation').annotate(count=Count('id'))
    return render(request, 'catalog/dashboard.html', {
        'orders': orders,
        'stats': stats
    })


# ✅ 新增：用户注册视图
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('star_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'catalog/register.html', {'form': form})
