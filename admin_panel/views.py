from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import models
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta

from myapp.forms import MobileAppForm
from myapp.models import Volunteer, Donation, ContactMessage, Profile



def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('/admin/dashboard/')

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username).first()
            if not user_obj:
                messages.info(request, 'Account not found')
                return redirect(request.META.get('HTTP_REFERER', '/'))

            user_obj = authenticate(username=username, password=password)
            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('/admin/dashboard/')
            else:
                messages.info(request, 'Invalid credentials or not an admin')
                return redirect('/')

        return render(request, 'admin_login.html')

    except Exception as e:
        print(f"Login error: {e}")
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return redirect('/')

def admin_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('admin_login')   

def sample(request) :
    return render(request, 'sample-page.html')

# views.py

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_dashboard(request):
    # Summary counts
    total_users = Profile.objects.count()
    total_volunteers = Volunteer.objects.count()
    total_donations = Donation.objects.filter(paid=True).aggregate(total=Sum('amount'))['total'] or 0

    # Recent donations (fallback if none are paid)
    recent_donations = Donation.objects.filter(paid=True).order_by('-created_at')[:6]
    if not recent_donations.exists():
        recent_donations = Donation.objects.order_by('-created_at')[:6]  # fallback for testing

    donation_labels = [don.created_at.strftime('%b %d') for don in recent_donations]
    donation_data = [float(don.amount) for don in recent_donations]
    donor_names = [don.name for don in recent_donations]

    # Monthly donation summary (last 6 months)
    months = []
    monthly_data = []
    for i in range(5, -1, -1):
        month_date = now() - timedelta(days=30*i)
        month_name = month_date.strftime('%b')
        total = Donation.objects.filter(
            paid=True,
            created_at__month=month_date.month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        months.append(month_name)
        monthly_data.append(float(total))

    # Recent messages
    recent_messages = ContactMessage.objects.order_by('-date_sent')[:5]

    context = {
        'total_users': total_users,
        'total_volunteers': total_volunteers,
        'total_donations': total_donations,
        'recent_donations': recent_donations,
        'donation_labels': donation_labels,
        'donation_data': donation_data,
        'donor_names': donor_names,
        'monthly_labels': months,
        'monthly_data': monthly_data,
        'recent_messages': recent_messages,
    }

    return render(request, 'dashboard.html', context)
@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_user(request):
    users = Profile.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'admin_user.html', context)

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_donation(request):
    donations = Donation.objects.all().order_by('-created_at')
    context = {
        'donations': donations,
    }
    return render(request, 'admin_donation.html', context)

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_messages(request):
    messages = ContactMessage.objects.all().order_by('-date_sent')
    context = {
        'messages': messages,
    }
    return render(request, 'admin_messages.html', context)


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_volunteer(request):
    volunteers = Volunteer.objects.all().order_by('-date_applied')
    context = {
        'volunteers': volunteers,
    }
    return render(request, 'admin_voluntear.html', context)

from django.shortcuts import render, redirect
from myapp.forms import MobileAppForm
from myapp.models import MobileApp

def admin_mobile_app(request):
    if request.method == 'POST':
        form = MobileAppForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_mobile_app')
    else:
        form = MobileAppForm()

    latest_apk = MobileApp.objects.latest('uploaded_at') if MobileApp.objects.exists() else None
    return render(request, 'admin_mobile_app.html', {'form': form, 'latest_apk': latest_apk})



