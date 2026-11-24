from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        field = ["id", "title", "amount", "category", "date"]
        read_only_fields = ["id"]


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.charField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validate_password)