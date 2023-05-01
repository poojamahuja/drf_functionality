from rest_framework import serializers
from .models import Company, Employee
from rest_framework.exceptions import ValidationError
from common_config.message import (USER_CONFIRM_PASSWORD_NOT_MATCH)
from django.contrib.auth.password_validation import validate_password


class CompanyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name",)


class EmployeeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "full_name", "profile_picture", "company", "email", "age")


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for validating, creating employee table data"""
    first_name = serializers.CharField(min_length=3, max_length=50)
    last_name = serializers.CharField(min_length=3, max_length=50)
    password = serializers.CharField(min_length=8, max_length=255,
                                     write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(min_length=8, max_length=255,
                                             required=False, write_only=True)

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'password', 'confirm_password', 'email')
        read_only_fields = ('username',)

    def validate(self, validated_data):
        """validate password and email format"""
        errors = {}
        # Password validation
        if "password" in validated_data:
            try:
                validate_password(validated_data['password'])
                if validated_data['password'] != validated_data['confirm_password']:
                    errors.setdefault("confirm_password", []).append(
                        USER_CONFIRM_PASSWORD_NOT_MATCH.format(
                            validated_data['confirm_password']))
            except Exception as err:
                errors.setdefault("password", []).append(err.args[0])

        if len(errors) > 0:
            # Raise exception
            raise ValidationError(errors)

        return validated_data

    def create(self, validated_data):
        user = Employee.objects.create(
            email=validated_data['email']
        )

        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.set_password(validated_data['password'])
        user.save()

        return user
