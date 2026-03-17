from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Transaction
from django.utils import timezone


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        help_texts = {
            'category': 'Select a category from the available list.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            if 'form-control' not in existing_class and 'form-select' not in existing_class:
                field.widget.attrs['class'] = f'{existing_class} form-control'.strip()

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        date = cleaned_data.get('date')
        category = cleaned_data.get('category')
        if amount is not None and amount <= 0:
            self.add_error('amount', 'Amount must be positive!')
        if date is not None and date > timezone.now().date():
            self.add_error('date', 'Date cannot be in the future!')
        if category is None:
            self.add_error('category', 'You must select a category.')
        return cleaned_data


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
