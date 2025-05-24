from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(email_type, data):
    if email_type == "volunteer":
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        age = data.get("age")
        profession = data.get("profession")
        message = data.get("message", "")

        # Email to admin
        send_mail(
            subject=f"New Volunteer Application - {name}",
            message=f"""Dear Admin,

A new volunteer application has been received.

Name: {name}
Email: {email}
Phone: {phone}
Age: {age}
Profession: {profession}

Message: {message}

Best Regards,
HumbleHandFoundation System""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['contactdarshan07@gmail.com'],
            fail_silently=False
        )

        # Email to volunteer
        send_mail(
            subject="Thank You for Volunteering with HumbleHandFoundation",
            message=f"""Dear {name},

Thank you for your interest in volunteering with HumbleHandFoundation. We have received your application and will review it shortly.

Best Regards,
HumbleHandFoundation Team""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

    elif email_type == "contact":
        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")

        # Email to admin
        send_mail(
            subject=f"New Contact Message - {subject}",
            message=f"""Dear Admin,

A new contact message has been received.

Name: {name}
Email: {email}
Subject: {subject}

Message: {message}

Best Regards,
HumbleHandFoundation System""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['contactdarshan07@gmail.com'],
            fail_silently=True
        )

        # Email to user
        send_mail(
            subject="Thank you for contacting Humble Hand Foundation",
            message=f"""Dear {name},

Thank you for reaching out to Humble Hand Foundation. We have received your message and will get back to you soon.

Best Regards,
Humble Hand Foundation Team""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=True
        )
        
    elif email_type == "reply":
        email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=True
        )

