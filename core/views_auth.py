import smtplib

from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView
from .forms import RegisterForm, SimplePasswordResetForm

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            send_mail(
                'Money Manager registration confirmation',
                f'Hello {self.object.username}, your registration was completed successfully.',
                settings.DEFAULT_FROM_EMAIL,
                [self.object.email],
                fail_silently=False,
            )
            messages.success(self.request, 'Account created successfully. A confirmation email was prepared.')
        except (smtplib.SMTPException, OSError):
            messages.warning(
                self.request,
                'Account created successfully, but the confirmation email could not be sent. Check email settings.',
            )
        return response


class SimplePasswordResetView(FormView):
    form_class = SimplePasswordResetForm
    template_name = 'registration/custom_password_reset_form.html'
    success_url = reverse_lazy('password-reset-done')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SimplePasswordResetDoneView(TemplateView):
    template_name = 'registration/custom_password_reset_done.html'
