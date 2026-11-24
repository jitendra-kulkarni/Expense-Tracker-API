
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Expense, Budget

from django.utils import timezone
from .serializers import ExpenseSerializer, RegisterSerializer
from django.contrib.auth.password_validation import validate_password


today = date.today()

# Create your views here.

class ExpenseListCreateView(generic.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.Isauthenticated]

    def get_queryset(self):
        return Expense.objects.filter(
            user=self.request.user
        ).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterAPIView(generic.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginAPIView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class RefreshTokenAPIView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


def logout_page(request):

    logout(request)

    return redirect('login_page')



def delete_expense(request, id):
    expense = Expense.objects.get(id=id,
        user=request.user
    )
    expense.delete()
    return redirect('home')


def edit_expense(request, id):
    expense = Expense.objects.get(id=id, 
        user=request.user
    )
    if request.method == 'POST':
        expense.title = request.POST.get('title')
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.date = request.POST.get('date')

        expense.save()

        return redirect('home')
    
    return render(request, 'edit_expense.html',{
        'expense':expense
    })


def update_budget(request):
    current_month = timezone.now().month
    current_year = timezone.now().year

    budget = Budget.objects.filter(
        user=request.user,
        month=current_month,
        year=current_year
    ).first()

    if request.method == 'POST':

        amount = request.POST.get('amount')
        if budget:

            budget.amount = amount
            budget.save()

        else:
            Budget.objects.create(
                user=request.user,
                amount=amount,
                month=current_month,
                year=current_year
            )

        return redirect('/')
    
    return render(request, 'budget.html',{
        "budget":budget
    })


from rest_framework import generic