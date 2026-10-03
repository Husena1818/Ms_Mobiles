from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail

from .models import RepairBooking, Accessory


def home(request):

    if request.method == 'POST':

        booking = RepairBooking.objects.create(
            customer_name=request.POST.get('customer_name'),
            customer_email=request.POST.get('customer_email'),
            phone_number=request.POST.get('phone_number'),
            mobile_brand=request.POST.get('mobile_brand'),
            mobile_model=request.POST.get('mobile_model'),
            problem_type=request.POST.get('problem_type'),
            problem_description=request.POST.get('problem_description'),
            visit_type=request.POST.get('visit_type'),
            preferred_date=request.POST.get('preferred_date'),
            phone_image=request.FILES.get('phone_image'),
        )

        # Email notification to MS Mobiles
        send_mail(
            subject='New Repair Booking - MS Mobiles',
            message=(
                f'New repair booking received.\n\n'
                f'Customer: {booking.customer_name}\n'
                f'Email: {booking.customer_email}\n'
                f'Phone: {booking.phone_number}\n'
                f'Device: {booking.mobile_brand} {booking.mobile_model}\n'
                f'Problem: {booking.problem_type}\n'
                f'Visit Type: {booking.visit_type}\n'
                f'Preferred Date: {booking.preferred_date}\n'
                f'Description: {booking.problem_description}\n'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # Confirmation email to customer
        if booking.customer_email:

            send_mail(
                subject='Repair Booking Confirmed - MS Mobiles',
                message=(
                    f'Hello {booking.customer_name},\n\n'
                    f'Your repair booking has been successfully submitted.\n\n'
                    f'Repair ID: #{booking.id}\n'
                    f'Mobile: {booking.mobile_brand} {booking.mobile_model}\n'
                    f'Problem: {booking.problem_type}\n'
                    f'Visit Type: {booking.visit_type}\n'
                    f'Preferred Date: {booking.preferred_date}\n\n'
                    f'Please keep your Repair ID to track your repair status.\n\n'
                    f'Thank you,\n'
                    f'MS Mobiles'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.customer_email],
                fail_silently=False,
            )

        return render(
            request,
            'mobiles/home.html',
            {
                'accessories': Accessory.objects.all().order_by('-created_at'),
                'booking_success': True,
                'repair_id': booking.id,
            }
        )

    accessories = Accessory.objects.all().order_by('-created_at')

    return render(
        request,
        'mobiles/home.html',
        {
            'accessories': accessories,
        }
    )


def track_repair(request):

    booking = None
    repair_id = request.GET.get('repair_id')

    if repair_id:
        try:
            booking = RepairBooking.objects.get(id=repair_id)
        except RepairBooking.DoesNotExist:
            booking = None

    return render(
        request,
        'mobiles/track_repair.html',
        {
            'booking': booking,
            'repair_id': repair_id,
        }
    )


def sitemap(request):

    return render(
        request,
        'sitemap.xml',
        content_type='application/xml'
    )