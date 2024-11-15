from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here
# Create adress table
class Address(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district= models.CharField(max_length=255)
    class Meta:
        unique_together = ('country', 'city', 'district')
    def __str__(self):
        return f"{self.country},{self.city},{self.district}"
    
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Email is used as the unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']  # These fields are required when creating a superuser

    def __str__(self):
        return self.email
    
class Login(models.Model):
    user= models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(unique=True, null=False)
    password = models.EmailField(unique=True, null=False)

    def __str__(self):
        return self.email
    
class Permission(models.Model):
    permission_id  = models.IntegerField(primary_key=True)
    role_id = models.ForeignKey(Role, null=False)
    def __str__(self):
        return self.permission_id
