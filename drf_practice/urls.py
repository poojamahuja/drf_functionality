from django.urls import path
from .views import CreateEmployeeView, login, EmployeeListApiView, update_employee, delete_employee, CompanyListApiView, \
    update_company, delete_company, add_employee, add_company

urlpatterns = [
    path('register', CreateEmployeeView.as_view(), name='register'),
    path('login', login),
    path('employee-detail', EmployeeListApiView.as_view()),
    path('create-employee', add_employee, name='add_employee'),
    path('update/<int:emp_id>', update_employee, name='update_employee'),
    path('delete/<int:emp_id>', delete_employee, name='delete_employee'),
    path('company-detail', CompanyListApiView.as_view()),
    path('create-company', add_company, name='add_company'),
    path('company-update/<int:company_id>', update_company, name='update_company'),
    path('company-delete/<int:company_id>', delete_company, name='delete_company'),
]
