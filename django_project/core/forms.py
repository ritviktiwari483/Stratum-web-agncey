from django import forms
from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'country', 'service', 'budget', 'timeline', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Full Name *',
                'class': 'form-input w-full border border-gray-300 rounded-2xl px-5 md:px-6 py-3.5 md:py-4 outline-none text-sm md:text-base',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Business Email *',
                'class': 'form-input w-full border border-gray-300 rounded-2xl px-5 md:px-6 py-3.5 md:py-4 outline-none text-sm md:text-base',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone Number with Country Code * (e.g. +1 234 567 890)',
                'class': 'form-input w-full border border-gray-300 rounded-2xl px-5 md:px-6 py-3.5 md:py-4 outline-none text-sm md:text-base',
            }),
            'country': forms.TextInput(attrs={
                'placeholder': 'Your Country (e.g. India, USA, UK)',
                'class': 'form-input w-full border border-gray-300 rounded-2xl px-5 md:px-6 py-3.5 md:py-4 outline-none text-sm md:text-base',
            }),
            'service': forms.Select(attrs={
                'class': 'form-input w-full border border-gray-300 rounded-2xl px-5 md:px-6 py-3.5 md:py-4 outline-none text-sm md:text-base',
            }),
            'budget': forms.Select(attrs={
                'class': 'form-input w-full border border-gray-300 rounded-2xl px-5 md:px-6 py-3.5 md:py-4 outline-none text-sm md:text-base',
            }),
            'timeline': forms.Select(attrs={
                'class': 'form-input w-full border border-gray-300 rounded-2xl px-5 md:px-6 py-3.5 md:py-4 outline-none text-sm md:text-base',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your project... *',
                'rows': 5,
                'class': 'form-input w-full border border-gray-300 rounded-3xl px-5 md:px-6 py-3.5 md:py-4 outline-none text-sm md:text-base',
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 2:
            raise forms.ValidationError('Name must be at least 2 characters.')
        return name.strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email is required.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError('Phone number is required so we can reach you quickly.')
        return phone.strip()

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 10:
            raise forms.ValidationError('Message must be at least 10 characters.')
        return message.strip()
