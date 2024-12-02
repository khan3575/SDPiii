from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model,authenticate,login
from .models import Address,Users,Login,Blog
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.utils.timezone import now

# Get the custom user model
User = get_user_model()

#Redirect to login if not authenticated
def redirect_home(request):
    return redirect('home')

#@login_required(login_url='/login/')
def home(request):
    blogs= Blog.objects.filter(status='published').order_by('-date','-time')
    return render(request, "home.html",{'blogs':blogs})

def signup(request):
    if request.method == 'POST':
        # Extract user details from form data
        user_email = request.POST.get('user_email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        country = request.POST.get('country')
        city = request.POST.get('city')
        district = request.POST.get('district')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "registration/signup.html", {
                'user_email': user_email,
                'first_name': first_name,
                'last_name': last_name,
                'country': country,
                'city': city,
                'district': district,
            })

        # Check if the email is already taken
        if User.objects.filter(email=user_email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "registration/signup.html", {
                'user_email': user_email,
                'first_name': first_name,
                'last_name': last_name,
                'country': country,
                'city': city,
                'district': district,
            })

        address, created = Address.objects.get_or_create(
            country=country,
            city=city,
            district=district
        )

        # Create the user
        try:
            # Create the address object

            user = User.objects.create_user(
                email=user_email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                address=address  # Link the address to the user
            )
            #hashing the password
            hashed_password =  make_password(password1)
            Login.objects.create(
                user=user,
                email=user_email,
                password= hashed_password
            )

            login(request, user)
            messages.success(request, "Your account has been created successfully.")
            return redirect('home')  # Redirect to the home page after successful signup
        except Exception as e:
            messages.error(request, f"An error occurred while creating the user: {str(e)}")
            return render(request, "registration/signup.html", {
                'user_email': user_email,
                'first_name': first_name,
                'last_name': last_name,
                'country': country,
                'city': city,
                'district': district,
            })

    # GET request, render the signup form
    return render(request, "registration/signup.html")

#log in
def login_view(request):
    if request.method =="POST":
        user_email = request.POST.get('user_email')
        password = request.POST.get('password')

        user = authenticate(request,email= user_email, password=password)
        try:
            login_entry = Login.objects.get(email=user_email)
            if check_password(password, login_entry.password):
                login(request,login_entry.user)
                messages.success(request, "You have successfully logged in.")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        except Login.DoesNotExist:
            messages.error(request,"Invalid email or password.")
        # if user is not None:
        #     login(request, user)
        #     messages.success(request,"You have successfully logged in.")
        #     return redirect('home/')
        # else:
        #     messages.error(request,"Invalid email or password")
        #     return render(request, "registration/login.html",{
        #         'user_email':user_email
        #     })
        
    return render(request,  "registration/login.html")
@login_required(login_url='/login/')
def following(request):
    return render(request, 'following.html')

def like_blog(request,blog_id):
    if request.method =='POST':
        blog= get_object_or_404(Blog, pk=blog_id)
        Reaction.obejects.create()

def show_blog(request,blog_id):
    blog= get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog_details.html',{'blog':blog})

@login_required(login_url='/login/')
def write_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        status = request.POST.get('status')
        if title and content and category:
            blog = Blog.objects.create(
                user_id= request.user,
                blog_title= title,
                text=content,
                category_name=category,
                date= now().date(),
                time= now().time(),
                status=status
            )
            blog.save()
            return redirect('home')
        else:
            return render(request, 'writeblog.html',{'error':'All field are required.'})
    return render(request, 'writeblog.html')    


@login_required(login_url='/login/')
def profile(request):
    if request.method == 'POST':
        # Handle profile update
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        profile_picture= request.FILES.get('profile_picture')
        
        if profile_picture:
            user.profile_picture =profile_picture
        user.save()
        messages.success(request, "Profile updated successfully!")
        return render(request, 'profile.html', {'user': user})
    return render(request, 'profile.html', {'user': request.user})

def about(request):
    # Team members data
    team_members = [
        {"name": "Sakib Khan", "id": "21225103290"},
        {"name": "Rifa Sanjida", "id": "21225103274"},
        {"name": "Jannatul Masruk Mukta", "id": "21225103311"},
        {"name": "Kishor Kumar Das", "id": "21225103295"},
        {"name": "Mostaq Shahoriar", "id": "21225103305"},
    ]
    return render(request, 'about.html', {'team_members': team_members})

def privacy_policy(request):
    return render(request, 'privacypolicy.html')

