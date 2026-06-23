from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

from .models import Profile, Post, Donation, Volunteer, ContactMessage
from .forms import SignupForm, LoginForm, UpdateProfileForm, DonationForm, VolunteerForm, ContactMessageForm
from django.db.models import Q
from django.conf import settings
import razorpay

import qrcode
import base64
from io import BytesIO

def home(request):
    if request.method == 'POST':
        donation_form = DonationForm(request.POST)
        volunteer_form = VolunteerForm(request.POST)

        if 'donate' in request.path:
            if donation_form.is_valid():
                donation_form.save()
                messages.success(request, "Donation form submitted. Proceed to payment.")
                return redirect('home')

        elif 'volunteer' in request.path:
            if volunteer_form.is_valid():
                volunteer_form.save()
                messages.success(request, "Thanks for volunteering!")
                return redirect('home')

    else:
        donation_form = DonationForm()
        volunteer_form = VolunteerForm()

    context = {
        'donation_form': donation_form,
        'volunteer_form': volunteer_form,
    }
    return render(request, 'home.html', context)

def navbar(request):
    return render(request, "navbar.html")

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def Login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Welcome back!")
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def Logout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('signup')

@login_required
def UpdateProfile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=profile, user=request.user)
    return render(request, 'update_profile.html', {'form': form})

def Search(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    return render(request, 'home.html', {
        'results': results,
        'query': query
    })

@login_required(login_url='/login/')
def user_profile(request):
    profile = request.user.profile
    donation_form = DonationForm()
    volunteer_form = VolunteerForm()
    return render(request, "profile.html", {
        "profile": profile,
        "donation_form": donation_form,
        "volunteer_form": volunteer_form
    })

@csrf_exempt
def Donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            amount = form.cleaned_data['amount']
            amount_paise = int(amount * 100)

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            order = client.order.create({
                "amount": amount_paise,
                "currency": "INR",
                "payment_capture": "1"
            })

            # Save donation with paid=False until payment confirmation
            Donation.objects.create(
                name=name,
                email=email,
                amount=amount,
                order_id=order['id'],
                paid=False
            )

            return JsonResponse({
                "order_id": order['id'],
                "amount": amount_paise,
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "name": name,
                "email": email,
            })
        else:
            return JsonResponse({"error": "Invalid form data."})
    return JsonResponse({"error": "Invalid request method."})

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            # Verify payment signature
            client.utility.verify_payment_signature(params_dict)

            # Get donation by order_id
            donation = get_object_or_404(Donation, order_id=razorpay_order_id)

            # Mark donation as paid and save payment_id
            donation.paid = True
            donation.payment_id = razorpay_payment_id
            donation.save()

            # Redirect user to receipt page to view donation receipt
            return redirect('donation_receipt', order_id=donation.order_id)

        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed. Please contact support.")
            return HttpResponse("Payment verification failed.", status=400)

        except Donation.DoesNotExist:
            messages.error(request, "Donation record not found. Please contact support.")
            return HttpResponse("Donation not found.", status=404)

    else:
        return HttpResponse("Invalid request method.", status=405)

def volunteer_view(request):
    if request.method == 'POST':
        # Access the Volunteer model properly here
        Volunteer.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            interest=request.POST['interest'],
        )
        # redirect or render success page
    return render(request, 'home.html')



@login_required
def donation_history_view(request):
    user_email = request.user.email
    donations = Donation.objects.filter(email=user_email).order_by('-created_at')

    context = {
        'donations': donations,
        'donation_form': DonationForm(),
        'volunteer_form': VolunteerForm(),
    }
    return render(request, 'donation_history.html', context)

@login_required
def message_history_view(request):
    user_messages = ContactMessage.objects.filter(user=request.user).order_by('-date_sent')
    context = {
        'messages': user_messages,
        'donation_form': DonationForm(),
        'volunteer_form': VolunteerForm(),
    }
    return render(request, 'message_history.html', context)

@login_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.user = request.user
            contact_message.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('message_history')
    else:
        form = ContactMessageForm()

    context = {
        'form': form,
        'donation_form': DonationForm(),
        'volunteer_form': VolunteerForm(),
    }
    return render(request, 'home.html', context)

@login_required
def donation_receipt_view(request, order_id):
    donation = get_object_or_404(Donation, order_id=order_id, email=request.user.email)
    
    # Generate QR code data — e.g., encode order ID and amount, or a URL
    qr_data = f"Order ID: {donation.order_id}\nAmount: ₹{donation.amount}\nName: {donation.name}"

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Convert to base64 string
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_image_b64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "receipt.html", {
        "donation": donation,
        "qr_image_b64": qr_image_b64,
    })

from django.shortcuts import render
from .models import MobileApp

def mobile_app_page(request):
    apk = MobileApp.objects.latest('uploaded_at')
    return render(request, 'mobile_app.html', {'apk': apk})

def download_apk(request):
    apk = MobileApp.objects.latest('uploaded_at')
    return redirect(apk.apk_file.url)


def water_conservation(request):
    return render(request, "water_conservation.html")

def pedh_lagao(request):
    return render(request, "pedh_lagao.html")

def green_campus(request):
    return render(request, "green_campus.html")

def tree_plantation(request):
    return render(request, "tree_plantation.html")

def water_event(request):
    return render(request, "water_event.html")

def excellence_award(request):
    return render(request, "excellence_award.html")

