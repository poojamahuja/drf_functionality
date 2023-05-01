from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password=None):
        """ Create super user"""

        user = self.model(
            email=email, is_staff=True,
            is_superuser=1
        )
        # set password in MD5 hash format
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, request=None, **kwargs):
        """ Create normal user"""

        user = self.model(
            username=kwargs['username']
        )

        if request is not None:
            request.user = user

        # set user fields value
        for key, item in kwargs.items():
            if "username" != key or "password" != key:
                setattr(user, key, item)

        # set password in MD5 hash format
        user.set_password(kwargs['password'])
        user.save(using=self._db)
        return user


class Employee(AbstractUser):
    """
    Model to save users details
    """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    full_name = models.CharField(max_length=150, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employee_company', null=True,
                                blank=True)
    email = models.EmailField(unique=True, max_length=150)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profile')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    age = models.IntegerField()

    objects = CustomUserManager()

    class Meta:
        db_table = 'auth_employee'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)
