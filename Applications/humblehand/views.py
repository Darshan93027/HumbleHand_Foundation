from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from threading import Thread
from .forms import VolunteerForm, ContactForm, SignupForm
from .models import Volunteer, Contact
from .utils import send_notification_email
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from Applications.humblehand.utils import send_notification_email
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'humblehand/index.html')

def about(request):
    return render(request, 'humblehand/about.html')

def donate(request):
    return render(request, 'humblehand/donate.html')

def events(request):
    return render(request, 'humblehand/events.html')

def gallery(request):
    return render(request, 'humblehand/gallery.html')

@csrf_protect
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            Thread(target=send_notification_email, args=("contact", {
                "name": contact.name,
                "email": contact.email,
                "subject": contact.subject,
                "message": contact.message
            })).start()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'humblehand/contact.html', {'form': form})

@csrf_protect
def join(request):
    if request.method == "POST":
        form = VolunteerForm(request.POST)
        if form.is_valid():
            volunteer = form.save(commit=False)
            if request.user.is_authenticated:
                volunteer.user = request.user
            volunteer.save()

            Thread(target=send_notification_email, args=("volunteer", {
                "name": volunteer.name,
                "email": volunteer.email,
                "phone": volunteer.phone,
                "age": volunteer.age,
                "profession": volunteer.profession,
                "message": volunteer.message
            })).start()

            messages.success(request, "Thank you for volunteering! We will contact you soon.")
            return redirect('thank_you')
    else:
        form = VolunteerForm()
    return render(request, 'humblehand/join.html', {'form': form})

def thank_you(request):
    return render(request, 'humblehand/thank_you.html')



def common_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged in successfully!")

            if user.is_staff:
                return redirect('Founder_dashboard')  # For staff users
            else:
                return redirect('dashboard')  # For normal users
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "Humblehand/login.html")  # Use a common login template

@csrf_protect
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create associated volunteer profile if needed
            if 'volunteer' in request.POST:
                Volunteer.objects.create(
                    user=user,
                    name=f"{user.first_name} {user.last_name}",
                    email=user.email,
                    phone="",  # These fields can be updated later
                    age=18,
                    profession="OTHER"
                )
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'humblehand/signup.html', {'form': form})

@login_required(login_url='/login/')
def dashboard(request):
    volunteers = Volunteer.objects.all().order_by('-date', '-time')
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, "humblehand/dashboard.html", {
        'volunteers': volunteers,
        'contacts': contacts
    })

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('index')