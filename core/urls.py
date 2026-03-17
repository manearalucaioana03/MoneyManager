from django.urls import path
from . import views
from .views_auth import RegisterView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/add/', views.TransactionCreateView.as_view(), name='transaction-add'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction-edit'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction-delete'),
]