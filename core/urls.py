from django.urls import path
from . import views
from .views_auth import RegisterView, SimplePasswordResetDoneView, SimplePasswordResetView

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('reset-password/', SimplePasswordResetView.as_view(), name='password-reset'),
    path('reset-password/done/', SimplePasswordResetDoneView.as_view(), name='password-reset-done'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category-add'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/add/', views.TransactionCreateView.as_view(), name='transaction-add'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction-edit'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction-delete'),
]