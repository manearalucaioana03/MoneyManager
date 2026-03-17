from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Category, Transaction
from django.utils import timezone


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            if 'form-control' not in existing_class and 'form-select' not in existing_class:
                field.widget.attrs['class'] = f'{existing_class} form-control'.strip()

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
            'category': 'Select a category from the available list or add a new one.'
        }

    def get_user_balance(self):
        if self.user is None:
            return 0

        transactions = Transaction.objects.filter(user=self.user)
        income_total = transactions.filter(category__is_income=True).aggregate(total=Sum('amount'))['total'] or 0
        expense_total = transactions.filter(category__is_income=False).aggregate(total=Sum('amount'))['total'] or 0
        balance = income_total - expense_total

        if self.instance and self.instance.pk:
            if self.instance.category and self.instance.category.is_income:
                balance -= self.instance.amount
            else:
                balance += self.instance.amount

        return balance

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

        if category is not None and amount is not None and not category.is_income:
            available_balance = self.get_user_balance()
            if amount > available_balance:
                self.add_error('amount', 'Expense cannot be greater than your current balance.')

        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_income']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_income': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if name and Category.objects.filter(name__iexact=name.strip()).exists():
            self.add_error('name', 'This category already exists.')
        return cleaned_data


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
