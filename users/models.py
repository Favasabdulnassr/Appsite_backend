from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin



class CustomUserManager(BaseUserManager):
    def create_user(self,email,phone_number,password=None,**extra_fields):
        if not email:
            raise ValueError("The email field is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email,phone_number=phone_number,password=password,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self,email,phone_number,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('role','admin')
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email,phone_number,password,**extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES = (
        ('user','User'),
        ('admin','Admin')
    )
    DEFAULT_ROLE = 'user'
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15,unique=True,blank=True,null=True,default=None)
    first_name = models.CharField(max_length=30,blank=True)
    last_name = models.CharField(max_length=30,blank=True)
    status = models.BooleanField(default=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default=DEFAULT_ROLE)
    total_points = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False) 


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        return f"{self.email} {self.id}"
    
    
