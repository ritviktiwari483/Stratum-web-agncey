from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from .models import Portfolio, SocialMedia
from .forms import ContactForm


def home(request):
    portfolios = Portfolio.objects.filter(is_active=True)
    social_links = SocialMedia.objects.filter(is_active=True)
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()

            # Email to admin
            try:
                admin_subject = f'New Lead: {submission.name} - {submission.country or "Unknown"}'
                admin_message = (
                    f'New Contact Form Submission\n'
                    f'{"="*40}\n'
                    f'Name: {submission.name}\n'
                    f'Email: {submission.email}\n'
                    f'Phone: {submission.phone}\n'
                    f'Country: {submission.country or "Not specified"}\n'
                    f'Service: {submission.get_service_display()}\n'
                    f'Budget: {submission.get_budget_display() or "Not specified"}\n'
                    f'Timeline: {submission.get_timeline_display() or "Not specified"}\n'
                    f'Message:\n{submission.message}\n'
                )
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=True,
                )

                # Thank-you email to client
                client_subject = 'Thank you for reaching out to StratumWeb Agency'
                client_message = (
                    f'Hi {submission.name},\n\n'
                    f'Thank you for contacting StratumWeb Agency!\n\n'
                    f'We have received your inquiry with the following details:\n'
                    f'Service: {submission.get_service_display()}\n'
                    f'Budget: {submission.get_budget_display() or "Flexible"}\n'
                    f'Timeline: {submission.get_timeline_display() or "Flexible"}\n'
                    f'Country: {submission.country or "Not specified"}\n\n'
                    f'Our team will review your message and get back to you '
                    f'within 24 hours via email or WhatsApp.\n\n'
                    f'In the meantime, feel free to check our portfolio at '
                    f'https://stratumweb.com\n\n'
                    f'Best regards,\n'
                    f'Ritvik Tiwari & Ayush Singh\n'
                    f'StratumWeb Agency'
                )
                send_mail(
                    client_subject,
                    client_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [submission.email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                'Thank you! Your message has been sent successfully. We will get back to you within 24 hours.'
            )
            form = ContactForm()
        else:
            messages.error(
                request,
                'Please fix the errors below and try again.'
            )

    return render(request, 'index.html', {
        'portfolios': portfolios,
        'social_links': social_links,
        'form': form,
    })
