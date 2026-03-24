from django.db.models import Sum

from .models import Transaction


def get_financial_summary(user):
	if not user.is_authenticated:
		return {
			'income_total': 0,
			'expense_total': 0,
			'current_balance': 0,
		}

	transactions = Transaction.objects.filter(user=user)
	income_total = transactions.filter(category__is_income=True).aggregate(total=Sum('amount'))['total'] or 0
	expense_total = transactions.filter(category__is_income=False).aggregate(total=Sum('amount'))['total'] or 0
	return {
		'income_total': income_total,
		'expense_total': expense_total,
		'current_balance': income_total - expense_total,
	}


def financial_summary(request):
	return get_financial_summary(request.user)