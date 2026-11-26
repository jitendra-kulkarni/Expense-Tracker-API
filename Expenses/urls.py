
from django.urls import path
from . import views

urlpatterns = [
   
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("token/refresh/", views.RefreshTokenAPIView.as_view(), name="token_refresh"),

   
    path("expenses/", views.ExpenseListCreateView.as_view(), name="expense-list-create"),
    path("expenses/<int:pk>/", views.ExpenseDetailAPIView.as_view(), name="expense-detail"),


    path("budgets/", views.BudgetListCreateAPIView.as_view(), name="budget-list-create"),
    path("budgets/<int:pk>/", views.BudgetDetailAPIView.as_view(), name="budget-detail"),
]
