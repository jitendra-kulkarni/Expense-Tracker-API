
from rest_framework import generics, permissions

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Budget

from .serializers import (
    ExpenseSerializer, 
    RegisterSerializer,
    BudgetSerializer,
)

from django.contrib.auth.password_validation import validate_password

# Create your views here.

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(
            user=self.request.user
        ).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginAPIView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class RefreshTokenAPIView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class BudgetListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(
            user=self.request.user
        ).order_by("-year", "-month")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

