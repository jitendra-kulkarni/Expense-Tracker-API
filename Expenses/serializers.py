from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Expense, Budget

class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = ["id", "title", "amount", "category", "date"]
        read_only_fields = ["id"]


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = ["id", "month", "year", "amount"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        user = self.context["request"].user

        month = attrs.get(
            "month",
            self.instance.month if self.instance else None
        )
        year = attrs.get(
            "year",
            self.instance.year if self.instance else None
        )

        budgets = Budget.objects.filter(
            user=user,
            month=month,
            year=year
        )

        if self.instance:
            budgets = budgets.exclude(pk=self.instance.pk)

        if budgets.exists():
            raise serializers.ValidationError({
                "month": "A budget for this month and year already exists."
            })

        return attrs

        
    