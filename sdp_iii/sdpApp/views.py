from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import get_user_model,authenticate,login
from .models import Address,Users,Login,Blog,Reaction,Comment,ActivityLog,Follow
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
    search_query = request.GET.get('search','')
    if search_query:
        blogs= Blog.objects.filter(blog_title__icontains=search_query)
    else:
        blogs= Blog.objects.all()

    blogs= blogs.filter(status='published').order_by('-date','-time')
    blog_data =  []
    for blog in blogs:
        like_count= Reaction.objects.filter(blog_id=blog, reaction_type='like').count()
        user_liked=False
        if request.user.is_authenticated:
            user_liked=Reaction.objects.filter(blog_id=blog, user_id=request.user, reaction_type='like').exists()
        blog_data.append({
            'blog':blog,
            'like_count':like_count,
            user_liked:user_liked,
        })
    
    return render(request, "home.html",{'blog_data':blog_data})

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
        
        
    return render(request,  "registration/login.html")

def forgot_password(request):
    if request.method == "POST":
        user_email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            # Check if the user exists in the Users table
            user = Users.objects.get(email=user_email)

            # Check if the user exists in the Login table
            login_entry = Login.objects.get(email=user_email)

            if new_password and confirm_password:
                if new_password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return render(request, 'forgetpassword.html', {"email": user_email})

                # Update the password in the Users table
                user.password = make_password(new_password)
                user.save()

                # Update the password in the Login table
                login_entry.password = make_password(new_password)
                login_entry.save()

                messages.success(request, "Password has been reset successfully.")
                return redirect('login')

            # If no password fields are provided, just validate the email
            return render(request, 'forgetpassword.html', {"email": user_email, "reset_mode": True})

        except Users.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return render(request, 'forgetpassword.html')

        except Login.DoesNotExist:
            messages.error(request, "No login record found for this email.")
            return render(request, 'forgetpassword.html')

    return render(request, 'forgetpassword.html')


def user_profile(request, user_id):
    # Fetch the user based on the ID
    user = get_object_or_404(Users, pk=user_id)
    
    if not user:
        raise HttpResponse("User not found")
    blogs = Blog.objects.filter(user_id=user)
    blogs= blogs.filter(status='published')

    is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    return render(request, 'user_profile.html', {'user': user, 'blogs': blogs,'is_following': is_following,})


@login_required(login_url='/login/')
def following(request):
    user = request.user

    follow_users = user.following.all()
    blogs = Blog.objects.filter(user_id__in=follow_users).filter(status='published').order_by('-date','-time')
    return render(request, 'following.html',{'blogs',blogs})



def blog_details(request,blog_id):
    blog= get_object_or_404(Blog, pk=blog_id)
    user_liked=False
    like_count= Reaction.objects.filter(blog_id=blog, reaction_type='like').count()
    if request.user.is_authenticated:
        user_liked= Reaction.objects.filter(blog_id=blog, user_id= request.user, reaction_type='like').exists()
    
    # Get the comment count for this blog
    comment_count = Comment.objects.filter(blog_id=blog).count()

    # Get the list of comments
    comments = Comment.objects.filter(blog_id=blog)

    return render(request, 'blog_details.html', {
        'blog': blog,
        'comments': comments,
        'like_count': like_count,
        'comment_count': comment_count,
        'user_liked' : user_liked,
    })

@login_required(login_url='/login/')
def write_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        status = request.POST.get('status')
        image= request.FILES.get('image')
        if title and content and category:
            blog = Blog.objects.create(
                user_id= request.user,
                blog_title= title,
                text=content,
                category_name=category,
                date= now().date(),
                time= now().time(),
                status=status,
                image=image
            )
            blog.save()
            return redirect('home')
        else:
            return render(request, 'writeblog.html',{'error':'All field are required.'})
    return render(request, 'writeblog.html')    


#edit profile view
@login_required(login_url='/login/')
def edit_profile(request):
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
        return render(request, 'editprofile.html', {'user': user})
    return render(request, 'editprofile.html', {'user': request.user})

#show  profile view
@login_required(login_url='/login/')
def profile_show(request):
    return render(request, 'showprofile.html', {'user': request.user})



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


#showing myblog lists

def myblogs(request):
    user_blogs = Blog.objects.filter(user_id=request.user.user_id).order_by('-date')
    return render(request, 'myblogs.html', {'user_blogs': user_blogs})


#adding a like 
@login_required
def like_blog(request, blog_id):
    if request.method == "POST":
        blog = Blog.objects.get(pk=blog_id)
        user = request.user

        # Check if the user has already liked the blog
        existing_reaction = Reaction.objects.filter(user_id=user, blog_id=blog, reaction_type='like').first()

        if existing_reaction:
            # If already liked, remove the like
            existing_reaction.delete()
            liked = False
        else:
            # Otherwise, add a like
            Reaction.objects.create(user_id=user, blog_id=blog, reaction_type='like')
            liked = True

        # Update like count
        like_count = Reaction.objects.filter(blog_id=blog, reaction_type='like').count()

        return JsonResponse({"liked": liked, "like_count": like_count})

    return HttpResponse(status=405)  # Method not allowed



@login_required
def get_comments(request, blog_id):
    comments = Comment.objects.filter(blog_id=blog_id).values('user_id__first_name', 'user_id__last_name', 'comments', 'date', 'time')
    
    comment_list = list(comments)  # Convert QuerySet to list
    return JsonResponse({'comments': comment_list})


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(Users, pk=user_id)
    
    # Check if the current user is not trying to follow themselves
    if request.user == user_to_follow:
        return redirect('profile', user_id=user_id)
    
    # Check if the user is already following
    existing_follow = Follow.objects.filter(follower=request.user, following=user_to_follow).first()
    
    if not existing_follow:
        # If not following, create a new follow record
        Follow.objects.create(follower=request.user, following=user_to_follow)
    else:
        # If already following, remove the follow record (unfollow)
        existing_follow.delete()

    return redirect('profile', user_id=user_id)  # Or any other page you want to redirect to

