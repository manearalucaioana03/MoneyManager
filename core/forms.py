from django import forms
from .models import Transaction
from django.utils import timezone

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'date', 'description']

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        date = cleaned_data.get('date')
        if amount is not None and amount <= 0:
            self.add_error('amount', 'Amount must be positive!')
        if date is not None and date > timezone.now().date():
            self.add_error('date', 'Date cannot be in the future!')
        return cleaned_data
