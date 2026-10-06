from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.http import HttpResponse

import os
import requests

from .models import RepairBooking, Accessory


def send_whatsapp_message(phone_number, message):

    phone_number_id = getattr(
        settings,
        "WHATSAPP_PHONE_NUMBER_ID",
        ""
    )

    access_token = getattr(
        settings,
        "WHATSAPP_ACCESS_TOKEN",
        ""
    )

    if not phone_number_id or not access_token:
        print(
            "WhatsApp notification skipped: "
            "credentials not configured."
        )
        return False

    clean_phone = "".join(
        character
        for character in str(phone_number)
        if character.isdigit()
    )

    if len(clean_phone) == 10:
        clean_phone = "91" + clean_phone

    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{phone_number_id}/messages"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "to": clean_phone,
        "type": "text",
        "text": {
            "body": message
        }
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=10
        )

        print(
            "WhatsApp API response:",
            response.status_code,
            response.text
        )

        if response.ok:
            print(
                "WhatsApp notification sent successfully."
            )
            return True

        print(
            "WhatsApp notification failed:",
            response.status_code,
            response.text
        )

        return False

    except Exception as e:

        print(
            "WhatsApp notification error:",
            e
        )

        return False


def send_booking_email(
    subject,
    message,
    recipient
):

    try:

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )

        print(
            f"Email sent successfully to {recipient}"
        )

        return True

    except Exception as e:

        print(
            f"Email failed for {recipient}:",
            e
        )

        return False


def home(request):

    if request.method == "POST":

        # Save booking first
        booking = RepairBooking.objects.create(

            customer_name=request.POST.get(
                "customer_name"
            ),

            customer_email=request.POST.get(
                "customer_email"
            ),

            phone_number=request.POST.get(
                "phone_number"
            ),

            mobile_brand=request.POST.get(
                "mobile_brand"
            ),

            mobile_model=request.POST.get(
                "mobile_model"
            ),

            problem_type=request.POST.get(
                "problem_type"
            ),

            problem_description=request.POST.get(
                "problem_description"
            ),

            visit_type=request.POST.get(
                "visit_type"
            ),

            preferred_date=request.POST.get(
                "preferred_date"
            ),

            phone_image=request.FILES.get(
                "phone_image"
            ),
        )

        print(
            f"Repair booking created successfully. "
            f"Repair ID: {booking.id}"
        )

        # WhatsApp notification
        whatsapp_message = (
            "🔧 MS MOBILES - New Repair Booking\n\n"
            f"Repair ID: #{booking.id}\n"
            f"Customer: {booking.customer_name}\n"
            f"Phone: {booking.phone_number}\n"
            f"Email: "
            f"{booking.customer_email or 'Not provided'}\n"
            f"Mobile: {booking.mobile_brand} "
            f"{booking.mobile_model}\n"
            f"Problem: {booking.problem_type}\n"
            f"Visit Type: {booking.visit_type}\n"
            f"Preferred Date: {booking.preferred_date}\n\n"
            f"Description:\n"
            f"{booking.problem_description}"
        )

        send_whatsapp_message(
            booking.phone_number,
            whatsapp_message
        )

        # Email to MS Mobiles
        admin_email = getattr(
            settings,
            "EMAIL_HOST_USER",
            ""
        )

        if admin_email:

            admin_email_message = (
                "New repair booking received.\n\n"
                f"Repair ID: #{booking.id}\n"
                f"Customer: {booking.customer_name}\n"
                f"Email: "
                f"{booking.customer_email or 'Not provided'}\n"
                f"Phone: {booking.phone_number}\n"
                f"Device: {booking.mobile_brand} "
                f"{booking.mobile_model}\n"
                f"Problem: {booking.problem_type}\n"
                f"Visit Type: {booking.visit_type}\n"
                f"Preferred Date: {booking.preferred_date}\n\n"
                f"Description:\n"
                f"{booking.problem_description}\n"
            )

            send_booking_email(
                "New Repair Booking - MS Mobiles",
                admin_email_message,
                admin_email
            )

        else:

            print(
                "Email skipped: EMAIL_HOST_USER "
                "is not configured."
            )

        # Confirmation email to customer
        if booking.customer_email:

            customer_message = (
                f"Hello {booking.customer_name},\n\n"
                "Your repair booking has been successfully "
                "submitted to MS Mobiles.\n\n"
                f"Repair ID: #{booking.id}\n"
                f"Mobile: {booking.mobile_brand} "
                f"{booking.mobile_model}\n"
                f"Problem: {booking.problem_type}\n"
                f"Visit Type: {booking.visit_type}\n"
                f"Preferred Date: {booking.preferred_date}\n\n"
                "Please keep your Repair ID to track "
                "your repair status.\n\n"
                "Thank you,\n"
                "MS Mobiles"
            )

            send_booking_email(
                "Repair Booking Confirmed - MS Mobiles",
                customer_message,
                booking.customer_email
            )

        # Success page
        return render(
            request,
            "mobiles/home.html",
            {
                "accessories": Accessory.objects.all().order_by(
                    "-created_at"
                ),
                "booking_success": True,
                "repair_id": booking.id,
            }
        )

    accessories = Accessory.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "mobiles/home.html",
        {
            "accessories": accessories,
        }
    )


def track_repair(request):

    booking = None

    repair_id = request.GET.get(
        "repair_id"
    )

    if repair_id:

        try:

            booking = RepairBooking.objects.get(
                id=repair_id
            )

        except RepairBooking.DoesNotExist:

            booking = None

    return render(
        request,
        "mobiles/track_repair.html",
        {
            "booking": booking,
            "repair_id": repair_id,
        }
    )


def sitemap(request):

    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

    <url>
        <loc>
            https://ms-mobiles-4us8.onrender.com/
        </loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>

    <url>
        <loc>
            https://ms-mobiles-4us8.onrender.com/track-repair/
        </loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>

</urlset>
"""

    return HttpResponse(
        sitemap_content,
        content_type="application/xml"
    )


def setup_admin(request):

    setup_key = os.getenv(
        "ADMIN_SETUP_KEY"
    )

    if request.GET.get("key") != setup_key:

        return HttpResponse(
            "Invalid setup key.",
            status=403
        )

    User = get_user_model()

    username = os.getenv(
        "ADMIN_USERNAME"
    )

    password = os.getenv(
        "ADMIN_PASSWORD"
    )

    if not username or not password:

        return HttpResponse(
            "ADMIN_USERNAME or ADMIN_PASSWORD is missing.",
            status=500
        )

    user, created = User.objects.get_or_create(
        username=username
    )

    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()

    return HttpResponse(
        f"Admin setup successful. Username: {username}"
    )


def indexnow_key(request, key):

    indexnow_key = os.getenv(
        "INDEXNOW_KEY",
        ""
    )

    if key != indexnow_key:

        return HttpResponse(
            "",
            status=404
        )

    return HttpResponse(
        indexnow_key,
        content_type="text/plain"
    )