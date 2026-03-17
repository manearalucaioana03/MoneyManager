from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from .models import Category, Transaction
from .forms import CategoryForm, TransactionForm


def home(request):
	return render(request, 'core/home.html')


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

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
	model = Transaction
	form_class = TransactionForm
	template_name = 'core/transaction_form.html'
	success_url = reverse_lazy('transaction-list')

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
