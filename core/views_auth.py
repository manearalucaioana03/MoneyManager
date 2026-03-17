from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterForm

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        send_mail(
            'Money Manager registration confirmation',
            f'Hello {self.object.username}, your registration was completed successfully.',
            settings.DEFAULT_FROM_EMAIL,
            [self.object.email],
            fail_silently=False,
        )
        return response
