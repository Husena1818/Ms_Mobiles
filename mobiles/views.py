from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import RepairRequest


# =========================================================
# HOME PAGE
# =========================================================

def home(request):
    return render(request, "mobiles/home.html")


# =========================================================
# SEND REPAIR BOOKING EMAIL
# =========================================================

def send_repair_booking_email(
    repair_id,
    customer_name,
    phone,
    device,
    problem,
    visit_type,
    preferred_date,
    description,
):
    subject = "New Repair Booking - MS Mobiles"

    message = f"""New repair booking received.

Repair ID: #{repair_id}

Customer: {customer_name}
Phone: {phone}
Device: {device}
Problem: {problem}
Visit Type: {visit_type}
Preferred Date: {preferred_date or "Not specified"}
Description: {description or "No description provided."}

Please check the MS Mobiles admin panel for more details.

Thank you,
MS Mobiles
"""

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=["haseenavadla23@gmail.com"],
    )

    email.send(fail_silently=False)


# =========================================================
# BOOK REPAIR
# =========================================================

def book_repair(request):

    if request.method == "POST":

        # -------------------------------------------------
        # Get form data
        # -------------------------------------------------

        customer_name = request.POST.get(
            "customer_name", ""
        ).strip()

        phone = request.POST.get(
            "phone", ""
        ).strip()

        device = request.POST.get(
            "device", ""
        ).strip()

        problem = request.POST.get(
            "problem", ""
        ).strip()

        visit_type = request.POST.get(
            "visit_type", ""
        ).strip()

        preferred_date = request.POST.get(
            "preferred_date", ""
        ).strip()

        description = request.POST.get(
            "description", ""
        ).strip()

        # -------------------------------------------------
        # Validation
        # -------------------------------------------------

        if not customer_name:
            messages.error(
                request,
                "Please enter customer name."
            )
            return render(
                request,
                "mobiles/book_repair.html"
            )

        if not phone:
            messages.error(
                request,
                "Please enter phone number."
            )
            return render(
                request,
                "mobiles/book_repair.html"
            )

        if not device:
            messages.error(
                request,
                "Please enter mobile device."
            )
            return render(
                request,
                "mobiles/book_repair.html"
            )

        if not problem:
            messages.error(
                request,
                "Please select the repair service."
            )
            return render(
                request,
                "mobiles/book_repair.html"
            )

        # -------------------------------------------------
        # Convert device into brand and model
        # -------------------------------------------------

        device_parts = device.split(maxsplit=1)

        if len(device_parts) == 2:
            brand = device_parts[0]
            mobile_model = device_parts[1]
        else:
            brand = device
            mobile_model = device

        # -------------------------------------------------
        # Convert repair problem to service choice
        # -------------------------------------------------

        service_map = {
            "Screen Replacement": "SCREEN",
            "Battery Replacement": "BATTERY",
            "Charging Repair": "CHARGING",
            "Speaker & Mic Repair": "SPEAKER",
            "Software Service": "SOFTWARE",
            "Hardware Repair": "HARDWARE",
            "Other": "OTHER",

            # In case the HTML sends the database values
            "SCREEN": "SCREEN",
            "BATTERY": "BATTERY",
            "CHARGING": "CHARGING",
            "SPEAKER": "SPEAKER",
            "SOFTWARE": "SOFTWARE",
            "HARDWARE": "HARDWARE",
            "OTHER": "OTHER",
        }

        service = service_map.get(
            problem,
            "OTHER"
        )

        # -------------------------------------------------
        # Create repair request
        # -------------------------------------------------

        repair = RepairRequest.objects.create(
            customer_name=customer_name,
            phone=phone,
            brand=brand,
            mobile_model=mobile_model,
            service=service,

            # Your existing database requires this field
            service_type=problem,

            problem_description=description,
            status="Pending",
        )

        # -------------------------------------------------
        # Send confirmation email
        # -------------------------------------------------

        try:

            send_repair_booking_email(
                repair_id=repair.id,
                customer_name=customer_name,
                phone=phone,
                device=device,
                problem=problem,
                visit_type=visit_type or "Shop Visit",
                preferred_date=preferred_date,
                description=description,
            )

            messages.success(
                request,
                f"Repair booking successful! "
                f"Your Repair ID is #{repair.id}. "
                f"Confirmation email has been sent."
            )

        except Exception as e:

            print("EMAIL ERROR:", e)

            messages.warning(
                request,
                f"Repair booking created successfully. "
                f"Your Repair ID is #{repair.id}, "
                f"but the email could not be sent."
            )

        return redirect("book_repair")

    # -----------------------------------------------------
    # GET request
    # -----------------------------------------------------

    return render(
        request,
        "mobiles/book_repair.html"
    )


# =========================================================
# REPAIR TRACKING
# =========================================================

# =========================================================
# REPAIR TRACKING
# =========================================================

def repair_tracking(request):

    repair = None
    searched = False

    # -----------------------------------------------------
    # GET request - Track using URL
    # Example:
    # /repair-track/?repair_id=35
    # -----------------------------------------------------

    if request.method == "GET":

        repair_id = request.GET.get(
            "repair_id", ""
        ).strip()

        if repair_id:

            searched = True

            try:

                repair = RepairRequest.objects.get(
                    id=int(repair_id)
                )

            except (
                RepairRequest.DoesNotExist,
                ValueError,
            ):

                repair = None

    # -----------------------------------------------------
    # POST request - Track using form
    # -----------------------------------------------------

    elif request.method == "POST":

        searched = True

        repair_id = request.POST.get(
            "repair_id", ""
        ).strip()

        phone = request.POST.get(
            "phone", ""
        ).strip()

        if repair_id:

            try:

                repair = RepairRequest.objects.get(
                    id=int(repair_id)
                )

                # If phone is entered, verify it
                if phone and repair.phone != phone:
                    repair = None

            except (
                RepairRequest.DoesNotExist,
                ValueError,
            ):

                repair = None

    return render(
        request,
        "mobiles/repair_tracking.html",
        {
            "repair": repair,
            "searched": searched,
        },
    )