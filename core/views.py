from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from .context_processors import get_financial_summary
from .models import Category, Transaction
from .forms import CategoryForm, TransactionForm


def home(request):
	return render(request, 'core/home.html')


@login_required
def profile(request):
	transactions = Transaction.objects.filter(user=request.user)
	financial_summary = get_financial_summary(request.user)
	context = {
		'recent_transactions': transactions.order_by('-date', '-created_at')[:5],
		'transaction_count': transactions.count(),
		'category_count': Category.objects.filter(transaction__user=request.user).distinct().count(),
		'income_total': financial_summary['income_total'],
		'expense_total': financial_summary['expense_total'],
		'balance': financial_summary['current_balance'],
	}
	return render(request, 'core/profile.html', context)


class CategoryCreateView(LoginRequiredMixin, CreateView):
	model = Category
	form_class = CategoryForm
	template_name = 'core/category_form.html'
	success_url = reverse_lazy('category-list')


class CategoryListView(LoginRequiredMixin, ListView):
	model = Category
	template_name = 'core/category_list.html'
	context_object_name = 'categories'

	def get_queryset(self):
		return Category.objects.all().order_by('name')

class TransactionCreateView(LoginRequiredMixin, CreateView):
	model = Transaction
	form_class = TransactionForm
	template_name = 'core/transaction_form.html'
	success_url = reverse_lazy('transaction-list')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
	model = Transaction
	form_class = TransactionForm
	template_name = 'core/transaction_form.html'
	success_url = reverse_lazy('transaction-list')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
	model = Transaction
	template_name = 'core/transaction_confirm_delete.html'
	success_url = reverse_lazy('transaction-list')

class TransactionDetailView(LoginRequiredMixin, DetailView):
	model = Transaction
	template_name = 'core/transaction_detail.html'

class TransactionListView(LoginRequiredMixin, ListView):
	model = Transaction
	template_name = 'core/transaction_list.html'
	context_object_name = 'transactions'

	def get_queryset(self):
		return Transaction.objects.filter(user=self.request.user).order_by('-date')
