from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Applications.humblehand.models import Volunteer, Contact, User
from Applications.humblehand.forms import SignupForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Applications.humblehand.utils import send_notification_email


def signup(request):
    #if request.user.is_authenticated and request.user.is_staff:
      #  return redirect('Founder_dashboard')
        
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('Founder_login')
    else:
        form = SignupForm()
    return render(request, "Founder/signup.html", {'form': form})

@login_required
def user_data(request):
    users = User.objects.all()
    return render(request, 'Founder/user_data.html', {'users': users})

@login_required
def volunteer_data(request):
    if not request.user.is_staff:
        return redirect('Founder_login')
    volunteers = Volunteer.objects.all().order_by('-date', '-time')
    return render(request, 'Founder/volunteers.html', {'volunteers': volunteers})

@login_required
def message_data(request):
    if not request.user.is_staff:
        return redirect('Founder_login')
    messages_qs = Contact.objects.all().order_by('-created_at')
    return render(request, 'Founder/messages.html', {'messages': messages_qs})

@login_required
def Dashboard(request):
    if not request.user.is_staff:
        return redirect('Founder_login')
        
    volunteer_count = Volunteer.objects.count()
    message_count = Contact.objects.count()
    user_count = User.objects.count()
    
    context = {
        'volunteer_count': volunteer_count,
        'message_count': message_count,
        'user_count': user_count,
    }
    return render(request, 'Founder/dashboard.html', context)

@login_required
def donation_data(request):
    if not request.user.is_staff:
        return redirect('Founder_login')
    return render(request, "Founder/donation_data.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect('Founder_login')



@login_required
def delete_message(request):
    if request.method == "POST" and request.user.is_staff:
        message_id = request.POST.get("id")
        try:
            message = Contact.objects.get(id=message_id)
            message.delete()
            return JsonResponse({'success': True})
        except Contact.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Message not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})



@csrf_exempt  # You can use @login_required and remove this if CSRF is handled
def send_reply(request):
    if request.method == "POST" and request.user.is_staff:
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        data = {
            "email": email,
            "subject": subject,
            "message": message,
        }

        try:
            send_notification_email("reply", data)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})