from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.conf import settings
from django.apps import apps
from django.contrib.auth.decorators import login_required
import json
from .forms import CustomUserCreationForm                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
import base64
import uuid
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError
from .models import UserSettings
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import fitz 
import concurrent.futures
import requests
from django.http import JsonResponse, FileResponse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os, requests
import fitz  
from PIL import Image
from django.http import StreamingHttpResponse


def navbar(request):
    return render(request, "navbar.html")

def Home(request):
    return render(request, "home.html")

# def search_category(request):
#     category = request.GET.get('category', 'general')
#     print(category)
#     if category == 'general':
#         return render(request, 'category.html', {
#             'category': category,
#             'data': None  # or some data based on the category
#         })
    
# def search_protein(request):
#     category = request.GET.get('category', 'protein') 
#     print(category)
#     if category == 'protein':
#         data = Albumin.objects.filter(category='protein')
#         return render(request, "search_protein.html", {
#             'category': category,
#             'data': data,
#         })

def search_category(request):
    # print(category)
    category = request.GET.get('category', 'general')
    print(category)
    data = Albumin.objects.filter(category = category)
    print(data)
    if category == 'general':
        return render(request, 'category.html', {
            'category': category,
            'data': Albumin.objects.all()  
        })
    else:
        # Handle other categories
        return render(request, 'category.html', {
            'category': category,
            'data': data  # Replace with appropriate data for other categories
        })

def Databases(request, id):
    data = Albumin.objects.get(id=id)
    return render(request, "Albumin.html", {"data": data, "category": data.category})

def new_file(request):
    return render(request, "Forms.html")

@login_required
def form_view(request):
    if request.method == 'POST':
        # Get category from hidden field or from the dropdown
        category = request.POST.get('category', 'general')

        # Retrieve other form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        subtitle = request.POST.get('subtitle')
        subcontent = request.POST.get('subcontent')
        image = request.FILES.get('image')

        # Check if subcontent exists and convert it back to a Python object
        if subcontent:
            subcontent = eval(subcontent)  # Convert the string back into a list of dicts

        # Create a new Albumin object and save to the database
        albumin = Albumin(
            title=title,
            description=description,
            sub_title=subtitle,
            sub_content=subcontent,
            image=image,
            category=category,
            updated_by=request.user  # Assuming user is logged in
        )
        albumin.save()

        # Redirect to a success page or home page
        return redirect('search_category')  # Redirect to search page or another success page

    else:
        # Render the form with initial category selected (optional)
        category = 'category'  # Default category for display
        return render(request, 'Forms.html', {'category': category})

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             messages.success(request, 'Login successful!')
#             return redirect('home')  # Redirect to home page after successful login
#         else:
#             messages.error(request, 'Invalid username or password.')
#             return render(request, 'login.html')  # Re-render the login page with error message
#     else:
#         return render(request, 'login.html')  # Render login form for GET request

    # Ensure only authenticated users' details are passed to the template
    # user = None
    # if request.user.is_authenticated:
    #     user = CustomUser.objects.get(id=request.user.id)

    # return render(request, 'login.html', {'user': user})

UserModel = get_user_model()  # This is an alternative to directly using `settings.AUTH_USER_MODEL`

# def register(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         phone_number = request.POST['phone_number']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         profile_picture = request.FILES.get('profile_picture')

#         if password1 != password2:
#             messages.error(request, "Passwords do not match!")
#             return redirect('register')

#         if UserModel.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists!")
#             return redirect('register')

#         user = UserModel.objects.create_user(username=username, email=email, password=password1)
#         user.save()

#         # Save profile image
#         if profile_picture:
#             profile = Profile.objects.create(user=user, phone_number=phone_number, profile_picture=profile_picture)
#             profile.save()

#         messages.success(request, "Registration successful! Please log in.")
#         return redirect('login')

#     return render(request, 'register.html')

def upload_json(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            try:
                data = json.load(uploaded_file)  # Load JSON data
                
                for item in data:  # Save each record to the database
                    JsonData.objects.create(
                        title=item.get("title"),
                        category=item.get("category"),
                        description=item.get("description"),
                        sub_title=item.get("subtitle"),
                        subtitle_content=item.get("subtitle_content"),
                        file_upload=item.get("file")  # Assuming file path is included in the JSON file
                    )
                
                return redirect("upload_json")
            
            except json.JSONDecodeError:
                return render(request, "uploads_json.html", {"error": "Invalid JSON file."})

    else:
        form = UploadFileForm()

    table_data = JsonData.objects.all()  # Fetch all uploaded data
    return render(request, "uploads_json.html", {"form": form, "table_data": table_data})

def json_detail(request, id):
    json_data = get_object_or_404(JsonData, id=id)
    return render(request, "json_detail.html", {"json_data": json_data})

def json_edit(request, id):
    json_data = get_object_or_404(JsonData, id=id)

    if request.method == "POST":
        form = JsonDataForm(request.POST, instance=json_data)

        if form.is_valid():
            # Handle the fields: title, category, description, and subtitle
            json_data.title = request.POST.get('title')
            json_data.category = request.POST.get('category')
            json_data.description = request.POST.get('description')
            json_data.sub_title = request.POST.get('sub_title')

            # Handle the serialized JSON data for the subtitle_content (key-value pairs)
            subcontent_keys = request.POST.getlist('subcontent_key[]')
            subcontent_values = request.POST.getlist('subcontent_value[]')

            if subcontent_keys and subcontent_values:
                subtitle_content = []
                for key, value in zip(subcontent_keys, subcontent_values):
                    subtitle_content.append({'key': key, 'value': value})

                # Convert the subtitle content into a JSON string and save it
                json_data.subtitle_content = json.dumps(subtitle_content)

            # Save the form data to the model
            json_data.save()  # Save manually to store the serialized subtitle_content

            # Redirect after successful form submission
            return redirect('upload_json')  # Replace 'upload_json' with the appropriate URL name

    else:
        form = JsonDataForm(instance=json_data)

    return render(request, 'json_edit.html', {'form': form})

def json_delete(request, id):
    json_data = get_object_or_404(JsonData, id=id)
    json_data.delete()
    return redirect('upload_json')

User = get_user_model()

# def sign_up(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         phone_number = request.POST.get("phone_number")
#         password1 = request.POST.get("password1")
#         password2 = request.POST.get("password2")
#         profile_picture = request.FILES.get("profile_picture")

#         # ✅ Check if passwords match
#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return render(request, "signup.html")

#         # ✅ Check if username, email, and phone number already exist
#         if CustomUser.objects.filter(username=username).exists():
#             messages.error(request, "Username already taken.")
#             return render(request, "signup.html")

#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, "Email already registered.")
#             return render(request, "signup.html")

#         if CustomUser.objects.filter(phone_number=phone_number).exists():
#             messages.error(request, "Phone number already in use.")
#             return render(request, "signup.html")

#         # ✅ Create new user
#         user = CustomUser.objects.create_user(
#             username=username,
#             email=email,
#             phone_number=phone_number,
#             password=password1,
#         )

#         # ✅ Create user profile
#         profile = Profile.objects.create(user=user)
#         if profile_picture:
#             profile.profile_picture = profile_picture
#             profile.save()

#         # ✅ Redirect to the login page with a success message
#         messages.success(request, "Registration successful! Please log in.")
#         return redirect("signin")  # Redirect to the login page

#     return render(request, "signup.html")

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        profile_picture = request.FILES.get("profile_picture")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect("signup")

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Redirect to the login page with empty input fields
        return redirect("signin")  # Make sure 'signin' is the correct URL name

    return render(request, "signup.html")

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Change "home" to your actual home page

        else:
            messages.error(request, "Invalid username or password")

    # Ensure no old data is carried over
    return render(request, "signin.html", {"image": None})
    
def logout_view(request):
    # Log the user out
    logout(request)
    # Redirect to the homepage or any other page
    return render(request, 'logout.html')  # or your desired URL

@login_required
def profile(request):
    user = request.user

    # Ensure the profile exists
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        try:
            # Handle profile picture upload 
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
                profile.save()

            # Handle username update (Check for duplicates)
            new_username = request.POST.get('username')
            if new_username and new_username != user.username:
                if CustomUser.objects.filter(username=new_username).exclude(id=user.id).exists():
                    messages.error(request, "This username is already taken. Please choose another.")
                    return redirect('profile')
                user.username = new_username

            # Handle email update (Check for duplicates)
            new_email = request.POST.get('email')
            if new_email and new_email != user.email:
                if CustomUser.objects.filter(email=new_email).exclude(id=user.id).exists():
                    messages.error(request, "This email is already in use. Please use another.")
                    return redirect('profile')
                user.email = new_email

            # Handle password update
            new_password = request.POST.get('password')
            if new_password:
                user.set_password(new_password)  # Hash the new password before saving
                user.save()

                # Authenticate the user with the new password
                updated_user = authenticate(username=user.username, password=new_password)
                if updated_user:
                    login(request, updated_user)  # Log in the user with the new password
                    messages.success(request, "Profile updated successfully! Please log in again.")
                    return redirect('signin')

            user.save()
            messages.success(request, "Profile updated successfully!")

            return redirect('profile')

        except IntegrityError:
            messages.error(request, "An error occurred while saving your profile. Please try again.")
            return redirect('profile')

    return render(request, 'profile.html')

from datetime import datetime
from django.utils.timezone import now
def setting(request):
    user_settings = UserSettings.objects.first()
    if not user_settings:
        user_settings = UserSettings.objects.create()

    return render(request, 'settings.html', {'user_settings': user_settings})

def update_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        # Authenticate user
        user = authenticate(username=request.user.username, password=current_password)

        if user:
            user.set_password(new_password)  # Secure password update
            user.save()
            return JsonResponse({"message": "Password updated successfully!"})
        else:
            return JsonResponse({"message": "Current password is incorrect!"}, status=400)

def save_settings(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_settings = UserSettings.objects.first()
            if not user_settings:
                user_settings = UserSettings.objects.create()

            # Update settings
            user_settings.date = data.get('date', now().date())
            user_settings.time = data.get('time', now().time())
            user_settings.timezone = data.get('timezone', user_settings.timezone)
            user_settings.language = data.get('language', user_settings.language)
            user_settings.save()

            return JsonResponse({
                "message": "Settings updated successfully!",
                "date": user_settings.date.strftime("%Y-%m-%d"),
                "time": user_settings.time.strftime("%H:%M:%S")
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

def submit_feedback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            feedback_text = data.get('feedback', '')

            user_settings = UserSettings.objects.first()
            if not user_settings:
                user_settings = UserSettings.objects.create()

            user_settings.feedback = feedback_text
            user_settings.save()

            return JsonResponse({"message": "Feedback submitted successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

def update_protein(request, id):
    data = Albumin.objects.get(id=id)
    print(data)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        sub_title = request.POST['subtitle']
        
        # Access the subcontent directly (it's already a list from the form)
        sub_content = json.loads(request.POST.get('subcontent', '[]'))
        
        # Check if the image is in the request files before accessing it
        image = request.FILES.get('image', None)

        # Update the model data with the new information
        data.title = title
        data.description = description
        data.sub_title = sub_title
        data.sub_content = sub_content
        
        # If there's a new image, update the image field
        if image:
            data.image = image
        
        # Save the updated data
        data.save()
        return redirect("search_category")
    return render(request, "update_protein.html", {'data': data})

def update_genome(request, id):
    data = Albumin.objects.get(id=id)
    print(data)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        sub_title = request.POST['subtitle']
        
        # Access the subcontent directly (it's already a list from the form)
        sub_content = json.loads(request.POST.get('subcontent', '[]'))
        
        # Check if the image is in the request files before accessing it
        image = request.FILES.get('image', None)

        # Update the model data with the new information
        data.title = title
        data.description = description
        data.sub_title = sub_title
        data.sub_content = sub_content
        
        # If there's a new image, update the image field
        if image:
            data.image = image
        
        # Save the updated data
        data.save()
        return redirect("search_category")
    return render(request, "update_genome.html", {'data': data})

def update_nucleotide(request, id):
    data = Albumin.objects.get(id=id)
    print(data)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        sub_title = request.POST['subtitle']
        
        # Access the subcontent directly (it's already a list from the form)
        sub_content = json.loads(request.POST.get('subcontent', '[]'))
        
        # Check if the image is in the request files before accessing it
        image = request.FILES.get('image', None)

        # Update the model data with the new information
        data.title = title
        data.description = description
        data.sub_title = sub_title
        data.sub_content = sub_content
        
        # If there's a new image, update the image field
        if image:
            data.image = image
        
        # Save the updated data
        data.save()
        return redirect("search_category")
    return render(request, "update_nucleotide.html", {'data': data})

def update_pubchem(request, id):
    data = Albumin.objects.get(id=id)
    print(data)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        sub_title = request.POST['subtitle']
        
        # Access the subcontent directly (it's already a list from the form)
        sub_content = json.loads(request.POST.get('subcontent', '[]'))
        
        # Check if the image is in the request files before accessing it
        image = request.FILES.get('image', None)

        # Update the model data with the new information
        data.title = title
        data.description = description
        data.sub_title = sub_title
        data.sub_content = sub_content
        
        # If there's a new image, update the image field
        if image:
            data.image = image
        
        # Save the updated data
        data.save()
        return redirect("search_category")
    return render(request, "update_pubchem.html", {'data': data})

def update_blast(request, id):
    data = Albumin.objects.get(id=id)
    print(data)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        sub_title = request.POST['subtitle']
        
        # Access the subcontent directly (it's already a list from the form)
        sub_content = json.loads(request.POST.get('subcontent', '[]'))
        
        # Check if the image is in the request files before accessing it
        image = request.FILES.get('image', None)

        # Update the model data with the new information
        data.title = title
        data.description = description
        data.sub_title = sub_title
        data.sub_content = sub_content
        
        # If there's a new image, update the image field
        if image:
            data.image = image
        
        # Save the updated data
        data.save()
        return redirect("search_category")
    return render(request, "update_blast.html", {'data': data})

def update_taxonomy(request, id):
    data = Albumin.objects.get(id=id)
    print(data)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        sub_title = request.POST['subtitle']
        
        # Access the subcontent directly (it's already a list from the form)
        sub_content = json.loads(request.POST.get('subcontent', '[]'))
        
        # Check if the image is in the request files before accessing it
        image = request.FILES.get('image', None)

        # Update the model data with the new information
        data.title = title
        data.description = description
        data.sub_title = sub_title
        data.sub_content = sub_content
        
        # If there's a new image, update the image field
        if image:
            data.image = image
        
        # Save the updated data
        data.save()
        return redirect("search_category")
    return render(request, "update_taxonomy.html", {'data': data})

def delete_protein(request, id):
    data=Albumin.objects.get(id=id)
    data.delete()
    return redirect("search_category")

def delete_genome(request, id):
    data=Albumin.objects.get(id=id)
    data.delete()
    return redirect("search_category")

def delete_nucleotide(request, id):
    data=Albumin.objects.get(id=id)
    data.delete()
    return redirect("search_category")

def delete_pubchem(request, id):
    data=Albumin.objects.get(id=id)
    data.delete()
    return redirect("search_category")

def delete_blast(request, id):
    data=Albumin.objects.get(id=id)
    data.delete()
    return redirect("search_category")

def delete_taxonomy(request, id):
    data=Albumin.objects.get(id=id)
    data.delete()
    return redirect("search_category")

#books
from django.shortcuts import render, redirect
# from .forms import BookForm, BookFileUploadForm
from .models import Book, BookFile

# def books_list(request):
#     books = Book.objects.all()

#     if request.method == "POST":
#         book_form = BookForm(request.POST, request.FILES)
#         file_form = BookFileUploadForm(request.POST, request.FILES)

#         if book_form.is_valid() and file_form.is_valid():
#             book = book_form.save()
#             file = file_form.save(commit=False)
#             file.book = book  # Associate file with the book if needed
#             file.save()
#             return redirect('books_list')  # Refresh the page after upload

#     else:
#         book_form = BookForm()
#         file_form = BookFileUploadForm()

#     return render(request, 'books.html', {'books': books, 'book_form': book_form, 'file_form': file_form})

from django.shortcuts import render
from .models import Book

from django.shortcuts import render
from django.conf import settings
from django.core.files import File
from .models import Book, BookFile
import os
import fitz  # PyMuPDF

# Ensure the covers directory exists
COVERS_DIRECTORY = os.path.join(settings.MEDIA_ROOT, 'covers')
os.makedirs(COVERS_DIRECTORY, exist_ok=True)

def extract_first_page_image(pdf_filename):
    """
    Extracts the first page of a PDF as an image and saves it in the covers/ directory.
    Returns the relative path to the image.
    """
    try:
        doc = fitz.open(pdf_filename)
        first_page = doc[0]
        pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Increase resolution

        cover_filename = os.path.splitext(os.path.basename(pdf_filename))[0] + ".png"
        cover_path = os.path.join(COVERS_DIRECTORY, cover_filename)

        pix.save(cover_path)

        if os.path.exists(cover_path):
            return f"static/covers/{cover_filename}"  # Return relative path
        else:
            return "covers/default_book.png"

    except Exception as e:
        print(f"Error extracting image from {pdf_filename}: {e}")
        return "covers/default_book.png"

def books(request):
    """
    Fetches books from the database, filters them by category and search query,
    and ensures each book has a cover image.
    """
    category = request.GET.get('category', '')  
    query = request.GET.get('q', '')

    books = Book.objects.all().prefetch_related('files')

    if category:
        books = books.filter(category__iexact=category)

    if query:
        books = books.filter(title__icontains=query)

    # Ensure every book has a cover image
    for book in books:
        if not book.image or book.image.name == "covers/default_book.png":
            print("AjayKumar")
            book_file = book.files.first()  # Get the first related file
            if book_file and book_file.file:
                print("Ajay")
                image_path = extract_first_page_image(book_file.file.path)
                if image_path and image_path != book.image.name:
                    with open(os.path.join(settings.MEDIA_ROOT, image_path), "rb") as img_file:
                        book.image.save(os.path.basename(image_path), File(img_file), save=True)

    return render(request, 'books.html', {'books': books, 'category': category})


# from django.shortcuts import render
# from django.http import JsonResponse
# from django.conf import settings
# from django.core.files import File
# import os
# from .models import Book  # Ensure you have imported your Book model

# def books(request):
#     """
#     Fetches books from the database, filters them by category and search query,
#     and ensures each book has a cover image.
#     """
#     category = request.GET.get('category', '')  
#     query = request.GET.get('q', '')

#     books = Book.objects.all().prefetch_related('files')

#     if category:
#         books = books.filter(category__iexact=category)

#     if query:
#         books = books.filter(title__icontains=query)

#     # Ensure every book has a cover image
#     for book in books:
#         if not book.image or book.image.name == "covers/default_book.png":
#             book_file = book.files.first()  # Get the first related file
#             if book_file and book_file.file:
#                 image_path = extract_first_page_image(book_file.file.path)
#                 if image_path and image_path != book.image.name:
#                     with open(os.path.join(settings.MEDIA_ROOT, image_path), "rb") as img_file:
#                         book.image.save(os.path.basename(image_path), File(img_file), save=True)

#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         book_list = [
#             {
#                 'title': book.title,
#                 'category': book.category,
#                 'image_url': book.image.url if book.image else '/media/covers/default_book.png'
#             }
#             for book in books
#         ]
#         return JsonResponse({'books': book_list})

#     return render(request, 'books.html', {'books': books, 'category': category})



import json
from django.shortcuts import render, redirect
from .models import Book, BookFile  # Ensure Book and BookFile models exist
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render, redirect
from .models import Book, BookFile

def upload_files(request):
    # Define categories
    category_choices = [
        ('Protein', 'Protein'),
        ('Genome', 'Genome'),
        ('Nucleotide', 'Nucleotide'),
        ('Taxonomy', 'Taxonomy'),
        ('PubChem', 'PubChem'),
        ('BLAST', 'BLAST'),
    ]

    if request.method == "POST":
        category = request.POST.get("category")  # Get selected category
        files = request.FILES.getlist("files")  # Get multiple uploaded files

        # Get the first book matching the category or create a new one
        book = Book.objects.filter(category=category).first()
        if not book:
            book = Book.objects.create(category=category, title=f"Default {category} Book")

        # Check if files were uploaded
        if not files:
            return render(request, "uploads.html", {
                "category_choices": category_choices,
                "error": "No files were uploaded. Please select files."
            })

        # Process and save uploaded files linked to the selected book
        for file in files:
            BookFile.objects.create(book=book, file=file)

        return redirect("upload_files")  # Redirect after successful upload

    return render(request, "uploads.html", {
        "category_choices": category_choices,
    })



# def upload_files(request):
#     if request.method == 'POST' and request.FILES.getlist('files'):
#         category = request.POST.get('category', 'Protein')
#         book_data = Book.objects.filter(category=category)
#         for uploaded_file in request.FILES.getlist('files'):  # Loop through multiple files
#             BookFile.objects.create(file=uploaded_file, book=book_data.first())  # Save each file as a separate entry
#         return redirect('upload_files')  # Reload the page to show uploaded files

#     books = BookFile.objects.all()  # Fetch all uploaded files from DB
#     return render(request, 'uploads.html', {'books': books})


# from django.shortcuts import render
# from django.conf import settings
# from .models import Book
# import os
# import fitz  # PyMuPDF
# from urllib.parse import urljoin

# # Ensure covers directory exists
# covers_directory = os.path.join(settings.MEDIA_ROOT, 'covers')
# os.makedirs(covers_directory, exist_ok=True)


# def extract_first_page_image(pdf_filename):
#     """Extracts the first page image of a PDF and saves it in covers/."""
#     try:
#         doc = fitz.open(pdf_filename)
#         first_page = doc[0]  # Get first page
#         pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Higher resolution

#         # Generate proper filename
#         cover_filename = os.path.splitext(os.path.basename(pdf_filename))[0] + ".png"
#         cover_path = os.path.join(covers_directory, cover_filename)  # Full path in MEDIA_ROOT

#         # Save the image
#         pix.save(cover_path)

#         # Store relative path in DB (Django will use MEDIA_URL)
#         return f"covers/{cover_filename}"

#     except Exception as e:
#         print(f"Error extracting image from {pdf_filename}: {e}")
#         return "covers/default_book.png"  # Store relative path for default image


# def books_list(request):
#     category = request.GET.get('category', '')  # Get category from URL
#     books = Book.objects.filter(category=category) if category else Book.objects.all()

#     for book in books:
#         if not book.image or book.image.name == "covers/default_book.png":  # Ensure the book has a file before processing
#             image = extract_first_page_image(book.file.path)
#             if image != book.image.name:  # Avoid unnecessary updates
#                 book.image = image  # Ensure relative path 'covers/filename.png'
#                 book.save(update_fields=['image'])

#     return render(request, 'books.html', {'books': books, 'category': category})

# Directory Setup
PDF_DIR = os.path.join(settings.BASE_DIR, 'Books')
COVERS_DIR = os.path.join(settings.BASE_DIR, 'static/covers')
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(COVERS_DIR, exist_ok=True)

# API keys
YOUTUBE_API_KEY = "AIzaSyAlk5VLBoiCD3TqxLS9HtMlyQZMgueX2NE"
GOOGLE_API_KEY = "AIzaSyCCLzb24E4fuJLwdeq94Zu9JPSkiozifso"
CUSTOM_SEARCH_ENGINE_ID = "c56f8f041442444b7"

# Home View
def home(request):
    return render(request, 'home.html')

# Immediate redirection after form submission
def search(request):
    search_word = request.GET.get('search_word', '').strip()
    if not search_word:
        return redirect('home')
    return redirect(f'/results/?search_word={search_word}')

# Results view
def results(request):
    search_word = request.GET.get('search_word', '').strip()
    return render(request, 'results.html', {'query': search_word})

# PDF Search (AJAX endpoint)
def search_pdf(request):
    search_word = request.GET.get('search_word', '').strip()

    def result_stream():
        book_found = False
        for result in search_pdfs(search_word):
            if "no_books_found" in result:
                yield f"data: {json.dumps(result)}\n\n"
                break
            yield f"data: {json.dumps(result)}\n\n"
            book_found = True
        
        if not book_found:
            yield f"data: {json.dumps({'no_books_found': True})}\n\n"

    return StreamingHttpResponse(result_stream(), content_type='text/event-stream')

# Google Search (AJAX endpoint)
def search_google(request):
    search_word = request.GET.get('search_word', '').strip()
    google_results = google_search(search_word)
    return JsonResponse({"google_results": google_results})

# YouTube Search (AJAX endpoint)
def search_youtube(request):
    search_word = request.GET.get('search_word', '').strip()
    youtube_results = fetch_youtube_results(search_word)
    return JsonResponse({"youtube_results": youtube_results})

# Optimized PDF Search Logic
def search_pdfs(search_word):  
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")][:100]

    # Title Matching for Faster Results
    for file in pdf_files:
        if search_word.lower() in file.lower():  
            yield {
                "book_name": file.replace(".pdf", ""),
                "book_cover": f"/static/covers/{file.replace('.pdf', '.png')}",
                "download_link": f"/download/{file}"
            }
            return  # Exit early once a title match is found

    def search_file(file):
        pdf_path = os.path.join(PDF_DIR, file)
        occurrences, cover_image = search_word_in_pdf(pdf_path, search_word)
        if occurrences > 0:
            return {
                "book_name": file.replace(".pdf", ""),
                "book_cover": cover_image if cover_image else "/static/default_cover.jpg",
                "download_link": f"/download/{file}"
            }
        return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(search_file, file): file for file in pdf_files}

        book_found = False
        for future in as_completed(futures):
            if book_found:
                break  # Stop further checks once a book is found

            try:
                result = future.result(timeout=3)  # Timeout for faster detection
                if result:
                    book_found = True
                    yield result  # Send result immediately
            except TimeoutError:
                print(f"Timeout error on file: {futures[future]}")
                continue

        if not book_found:
            yield {"no_books_found": True}

# PDF Search with Cover Extraction
def search_word_in_pdf(pdf_path, search_word):
    occurrences = 0
    cover_image_path = os.path.join(COVERS_DIR, os.path.basename(pdf_path).replace('.pdf', '.png'))

    if not os.path.exists(cover_image_path):
        try:
            with fitz.open(pdf_path) as doc:
                first_page = doc[0]
                pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))
                pix.save(cover_image_path)
        except Exception as e:
            print(f"Error extracting cover for {pdf_path}: {e}")
            cover_image_path = "/static/default_cover.jpg"

    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text = page.get_text()
                if search_word.lower() in text.lower():
                    occurrences += text.lower().count(search_word.lower())
                    if occurrences > 0:
                        break
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")

    return occurrences, cover_image_path

# Google Search Logic
def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={CUSTOM_SEARCH_ENGINE_ID}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])
        return [
            {
                "title": item["title"],
                "thumbnail": "/static/default_image.png",
                "download_link": item.get("link", "#")
            }
            for item in items[:5]
        ]
    except Exception:
        return []

# YouTube Search Logic
def fetch_youtube_results(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 5,
        "key": YOUTUBE_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return [
            {
                "title": item["snippet"]["title"],
                "thumbnail": "/static/default_thumbnail.jpg",
                "videoUrl": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            for item in data.get("items", [])
        ]
    except Exception:
        return []

# File Download
def download(request, book_name):
    pdf_path = os.path.join(PDF_DIR, book_name)
    if not os.path.exists(pdf_path):
        return JsonResponse({"error": "File not found."}, status=404)
    return FileResponse(open(pdf_path, 'rb'), as_attachment=True)

# Results view
def search_results(request):
    query = request.GET.get('search_word', '')
    context = {'query': query}
    return render(request, 'results.html', context)

# Results view
def search(request):
    search_word = request.GET.get('search_word', '').strip()
    return render(request, 'results.html', {'query': search_word})
