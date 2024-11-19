from django.db import models
from django.db.models import SET_NULL
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
class BlogDesc(models.Model):
    blog_desc_id = models.AutoField(primary_key=True)
    blog_desc_title = models.CharField(max_length=255, null=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    category_id = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    content_id = models.IntegerField()

    def __str__(self):
        return self.blog_desc_title
    
class Blog(models.Model):
    STATUS_CHOICES =[
        ('published','Published'),
        ('draft', 'Draft'),
        ('archived', 'Archived'),
    ]
    blog_id= models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    blog_desc = models.ForeignKey(BlogDesc, on_delete=SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    def __str__(self):
        return f"Blog {self.blog_id} by {self.user_id}"
    


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name
    
class Content(models.Model):
    content_id = models.AutoField(primary_key=True)
    text = models.TextField(null=False)
    image = models.ImageField(null=True)

    def __str__(self):
        return f"Content {self.content_id}"
    
class Comment(models.Model):
    STATUS_CHOICES = [
        ('visible', 'Visible'),
        ('hidden', 'Hidden'),
    ]

    comment_id = models.AutoField(primary_key=True)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    comments = models.TextField(null=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='visible')

    def __str__(self):
        return f"Comment {self.comment_id} by User {self.user_id}"
    
class Reaction(models.Model):
    REACTION_TYPES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('laugh', 'Laugh'),
        ('angry', 'Angry'),
    ]

    reaction_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES)

    class Meta:
        unique_together = ('user_id', 'blog_id', 'comment_id')  # Ensures unique reactions

    def __str__(self):
        return f"{self.reaction_type} by User {self.user_id}"

class ActivityLog(models.Model):
    ACTION_TYPES = [
        ('post_blog', 'Post Blog'),
        ('delete_comment', 'Delete Comment'),
        ('like', 'Like'),
        ('share', 'Share'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]

    log_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES, null=False)
    date_time = models.DateTimeField(null=False)

    def __str__(self):
        return f"Action {self.action_type} by User {self.user_id}"