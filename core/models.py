from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=100)
	is_income = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Category: {self.name} - Type: {'Income' if self.is_income else 'Expense'}"

class Transaction(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	date = models.DateField()
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def transaction_type(self):
		if self.category and self.category.is_income:
			return 'Income'
		return 'Expense'

	def signed_amount(self):
		if self.category and self.category.is_income:
			return self.amount
		return -self.amount

	def __str__(self):
		return f"Transaction: {self.amount} - {self.category.name if self.category else 'No Category'}"
