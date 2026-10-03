from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail

from .models import Mobile, Repair, Order


def home(request):
    mobiles_list = Mobile.objects.all().order_by('-id')[:6]

    return render(
        request,
        'mobiles/home.html',
        {'mobiles': mobiles_list}
    )


def mobiles(request):
    mobile_list = Mobile.objects.all().order_by('-id')

    return render(
        request,
        'mobiles/mobiles.html',
        {'mobiles': mobile_list}
    )


def mobile_detail(request, id):
    mobile = get_object_or_404(Mobile, id=id)

    return render(
        request,
        'mobiles/mobile_detail.html',
        {'mobile': mobile}
    )


def repair(request):

    if request.method == 'POST':

        customer_name = request.POST.get(
            'customer_name', ''
        ).strip()

        phone_number = request.POST.get(
            'phone_number', ''
        ).strip()

        mobile_brand = request.POST.get(
            'mobile_brand', ''
        ).strip()

        mobile_model = request.POST.get(
            'mobile_model', ''
        ).strip()

        imei_number = request.POST.get(
            'imei_number', ''
        ).strip()

        problem_type = request.POST.get(
            'problem_type',
            'Other'
        )

        problem = request.POST.get(
            'problem', ''
        ).strip()

        service_type = request.POST.get(
            'service_type',
            'Shop Visit'
        )

        phone_photo = request.FILES.get(
            'phone_photo'
        )

        repair = Repair.objects.create(
            customer_name=customer_name,
            phone_number=phone_number,
            mobile_brand=mobile_brand,
            mobile_model=mobile_model,
            imei_number=imei_number,
            problem_type=problem_type,
            problem=problem,
            phone_photo=phone_photo,
            service_type=service_type
        )

        print("========== REPAIR ID ==========")
        print(repair.id)
        print("================================")

        try:

            send_mail(
                subject=f'MS Mobiles - Repair Booked #{repair.id}',

                message=f"""
Hello {customer_name},

Your mobile repair has been successfully booked.

Repair ID: {repair.id}

Mobile:
{mobile_brand} {mobile_model}

Problem:
{problem_type}

Service Type:
{service_type}

Status:
{repair.status}

Please keep your Repair ID safe to track your repair.

Thank you,
MS Mobiles
""",

                from_email='reddyummadihema@gmail.com',

                recipient_list=[
                    'reddyummadihema@gmail.com'
                ],

                fail_silently=False
            )

        except Exception:
            pass

        return render(
            request,
            'mobiles/repair.html',
            {
                'success': True,
                'repair': repair,
                'repair_id': repair.id
            }
        )

    return render(
        request,
        'mobiles/repair.html'
    )


def track_repair(request):

    repair = None
    searched = False

    if request.method == 'POST':

        repair_id = request.POST.get(
            'repair_id', ''
        ).strip()

        searched = True

        if repair_id.isdigit():

            try:

                repair = Repair.objects.get(
                    id=int(repair_id)
                )

            except Repair.DoesNotExist:

                repair = None

    return render(
        request,
        'mobiles/track_repair.html',
        {
            'repair': repair,
            'searched': searched
        }
    )


def register(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username', ''
        ).strip()

        email = request.POST.get(
            'email', ''
        ).strip()

        password = request.POST.get(
            'password', ''
        )

        confirm_password = request.POST.get(
            'confirm_password', ''
        )

        if not username or not email or not password:

            messages.error(
                request,
                'Please fill all required fields.'
            )

            return render(
                request,
                'mobiles/register.html'
            )

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return render(
                request,
                'mobiles/register.html'
            )

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return render(
                request,
                'mobiles/register.html'
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return render(
            request,
            'mobiles/register.html',
            {'success': True}
        )

    return render(
        request,
        'mobiles/register.html'
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username', ''
        ).strip()

        password = request.POST.get(
            'password', ''
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'mobiles/login.html'
    )


def user_logout(request):

    logout(request)

    return redirect('home')


def cart(request):

    return render(
        request,
        'mobiles/cart.html'
    )


def place_order(request, id):

    if not request.user.is_authenticated:

        return redirect('login')

    mobile = get_object_or_404(
        Mobile,
        id=id
    )

    if request.method == 'POST':

        quantity = request.POST.get(
            'quantity',
            '1'
        )

        try:

            quantity = int(quantity)

            if quantity < 1:
                quantity = 1

        except ValueError:

            quantity = 1

        total_price = mobile.price * quantity

        order = Order.objects.create(
            customer=request.user,
            mobile=mobile,
            quantity=quantity,
            total_price=total_price
        )

        return render(
            request,
            'mobiles/order_success.html',
            {'order': order}
        )

    return render(
        request,
        'mobiles/place_order.html',
        {'mobile': mobile}
    )


def robots_txt(request):

    return render(
        request,
        'robots.txt',
        content_type='text/plain'
    )