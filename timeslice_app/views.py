from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Count, Sum
from decimal import Decimal
from .models import TimeSlice, Order, UserProfile
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm


def index(request):
    slices = TimeSlice.objects.all()
    return render(request, 'timeslice_app/index.html', {'slices': slices})


def search_timeslices(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = TimeSlice.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'timeslice_app/search_results.html', {
        'query': query,
        'results': results
    })


@login_required
def add_to_order(request, timeslice_id):
    timeslice = get_object_or_404(TimeSlice, id=timeslice_id)
    order = Order.objects.create(
        user=request.user,
        total_price=timeslice.price,
    )
    order.timeslices.add(timeslice)
    return redirect('order_success', order_id=order.id)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'timeslice_app/order_success.html', {'order': order})


def category_filter(request):
    category = request.GET.get('category')
    if category:
        results = TimeSlice.objects.filter(category=category)
    else:
        results = TimeSlice.objects.all()

    categories = TimeSlice.objects.values_list('category', flat=True).distinct()
    return render(request, 'timeslice_app/category_filter.html', {
        'results': results,
        'current_category': category,
        'categories': categories
    })


def location_filter(request):
    location = request.GET.get('location')
    if location:
        results = TimeSlice.objects.filter(location=location)
    else:
        results = TimeSlice.objects.all()

    locations = TimeSlice.objects.values_list('location', flat=True).distinct()
    return render(request, 'timeslice_app/location_filter.html', {
        'results': results,
        'current_location': location,
        'locations': locations
    })


def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    location = request.GET.get('location')
    sort = request.GET.get('sort')

    results = TimeSlice.objects.all()

    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        )

    if category:
        results = results.filter(category=category)
    if location:
        results = results.filter(location=location)

    if sort == 'price_asc':
        results = results.order_by('price')
    elif sort == 'price_desc':
        results = results.order_by('-price')
    elif sort == 'date_asc':
        results = results.order_by('historical_date')
    elif sort == 'date_desc':
        results = results.order_by('-historical_date')

    categories = TimeSlice.objects.values_list('category', flat=True).distinct()
    locations = TimeSlice.objects.values_list('location', flat=True).distinct()

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'timeslice_app/home.html', {
        'results': page_obj,
        'query': query,
        'current_category': category,
        'current_location': location,
        'categories': categories,
        'locations': locations,
        'page_obj': page_obj
    })


def timeslice_detail(request, timeslice_id):
    timeslice = get_object_or_404(TimeSlice, id=timeslice_id)
    return render(request, 'timeslice_app/timeslice_detail.html', {'item': timeslice})


def combined_filter(request):
    return redirect('home')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'timeslice_app/register.html', {'form': form})


@login_required
def user_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'timeslice_app/profile.html', {
        'profile': profile,
        'orders': orders
    })


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
@login_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    top_items = (
        Order.objects.values('timeslices__title')
        .annotate(order_count=Count('timeslices'))
        .order_by('-order_count')[:5]
    )
    total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

    return render(request, 'timeslice_app/admin_dashboard.html', {
        'total_orders': total_orders,
        'top_items': top_items,
        'total_revenue': total_revenue
    })


def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def custom_403(request, exception):
    return render(request, '403.html', status=403)