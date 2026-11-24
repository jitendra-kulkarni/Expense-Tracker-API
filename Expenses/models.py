
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Expense(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expenses"
    )
    title = models.CharField(max_length=100)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    category = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.title


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    year = models.IntegerField(
        validators=[MinValueValidator(2000)]
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "month", "year"],
                name="unique_user_monthly_budget"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}"
