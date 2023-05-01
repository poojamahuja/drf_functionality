from .models import Company, Employee
from .serializers import (EmployeeViewSerializer, EmployeeSerializer, CompanyViewSerializer)
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.generics import (CreateAPIView)
from common_config.utils import APIResponse, APIErrorResponse
from rest_framework import status
from common_config.message import (RECORD_CREATED, BAD_REQUEST, LOGIN_SUCCESS, INVALID_CREDENTIAL,
                                   RECORD_NOT_EXIST, RECORD_UPDATED, RECORD_DELETED)
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework import filters
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import serializers


# Create your views here.
class CreateEmployeeView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(serializer.data, status=status.HTTP_201_CREATED, custom_message=RECORD_CREATED)

        return APIErrorResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, custom_message=BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return APIErrorResponse({'error': 'Please provide both username and password'},
                                status=status.HTTP_400_BAD_REQUEST, custom_message=BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return APIResponse({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND,
                           custom_message=INVALID_CREDENTIAL)
    token, _ = Token.objects.get_or_create(user=user)
    return APIResponse({'token': token.key}, status=status.HTTP_200_OK, custom_message=LOGIN_SUCCESS)


class EmployeeListApiView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeViewSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email']
    ordering_fields = ['full_name', 'email']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


@api_view(['PUT'])
def update_employee(request, emp_id):
    try:
        emp = Employee.objects.get(pk=emp_id)
        data = EmployeeViewSerializer(instance=emp, data=request.data, partial=True)
        age = request.data['age']
        if age >= 18:
            if data.is_valid():
                data.save()
                return APIResponse(data.data, status=status.HTTP_200_OK, custom_message=RECORD_UPDATED)
            else:
                return APIErrorResponse(data.errors, status=status.HTTP_400_BAD_REQUEST, custom_message=BAD_REQUEST)
        else:
            return APIErrorResponse({}, status=status.HTTP_400_BAD_REQUEST,
                                    custom_message="Employee age can not be under 18.")
    except Employee.DoesNotExist:
        return APIErrorResponse(data={}, status=status.HTTP_404_NOT_FOUND, custom_message=RECORD_NOT_EXIST)


@api_view(['DELETE'])
def delete_employee(request, emp_id):
    try:
        emp = get_object_or_404(Employee, pk=emp_id)
        emp.delete()
        return APIResponse({}, status=status.HTTP_200_OK, custom_message=RECORD_DELETED)
    except Employee.DoesNotExist:
        return APIErrorResponse(data={}, status=status.HTTP_404_NOT_FOUND, custom_message=RECORD_NOT_EXIST)


class CompanyListApiView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyViewSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


@api_view(['PUT'])
def update_company(request, company_id):
    try:
        company = Company.objects.get(pk=company_id)
        data = CompanyViewSerializer(instance=company, data=request.data, partial=True)
        if data.is_valid():
            data.save()
            return APIResponse(data.data, status=status.HTTP_200_OK, custom_message=RECORD_UPDATED)
        else:
            return APIErrorResponse(data.errors, status=status.HTTP_400_BAD_REQUEST, custom_message=BAD_REQUEST)
    except Employee.DoesNotExist:
        return APIErrorResponse(data={}, status=status.HTTP_404_NOT_FOUND, custom_message=RECORD_NOT_EXIST)


@api_view(['DELETE'])
def delete_company(request, company_id):
    try:
        company = get_object_or_404(Company, pk=company_id)
        company.delete()
        return APIResponse({}, status=status.HTTP_200_OK, custom_message=RECORD_DELETED)
    except Company.DoesNotExist:
        return APIErrorResponse(data={}, status=status.HTTP_404_NOT_FOUND, custom_message=RECORD_NOT_EXIST)


@api_view(['POST'])
def add_employee(request):
    emp = EmployeeViewSerializer(data=request.data)

    # validating for already existing data
    if Employee.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    age = request.data['age']
    if age >= 18:
        if emp.is_valid():
            emp.save()
            return APIResponse(emp.data, status=status.HTTP_201_CREATED, custom_message=RECORD_CREATED)
        else:
            return APIErrorResponse(emp.errors, status=status.HTTP_400_BAD_REQUEST, custom_message=BAD_REQUEST)
    else:
        return APIErrorResponse({}, status=status.HTTP_400_BAD_REQUEST,
                                custom_message="Employee age can not be under 18.")


@api_view(['POST'])
def add_company(request):
    company = CompanyViewSerializer(data=request.data)

    # validating for already existing data
    if Company.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if company.is_valid():
        company.save()
        return APIResponse(company.data, status=status.HTTP_201_CREATED, custom_message=RECORD_CREATED)
    else:
        return APIErrorResponse(company.errors, status=status.HTTP_400_BAD_REQUEST, custom_message=BAD_REQUEST)
