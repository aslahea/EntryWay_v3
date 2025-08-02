from .models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import UserBioForm


@csrf_protect
@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, "Both username and password are required.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_deleted:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('home')
            else:
                messages.error(request, "Your account has been deactivated.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


@csrf_protect
@never_cache
def welcome_view(request):
    return render(request, 'welcome.html')


User = get_user_model()

# User registration details:
# Username: Ayoob
# Email: ayoob@gmail.com
# Password: ru_NW-r8epGeVQK
# confirm Password: ru_NW-r8epGeVQK
# dob: 2025-07-08
# gender: Male
# marital_status: Single
# agree_to_terms: on


@csrf_protect
@never_cache
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        dob = request.POST.get('dob', '')
        gender = request.POST.get('gender', '')
        marital_status = request.POST.get('marital_status', '')
        terms = request.POST.get('terms', '')

        # change gender setting
        if gender not in ['Male', 'Female', 'Other']:
            messages.error(request, "Malformed gender value")
            return redirect('register')

        # Server-side validations
        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric.")
            return redirect('register')

        if len(password1) < 8:
            messages.error(
                request, "Password must be at least 8 characters long.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        if terms != 'on':
            messages.error(
                request, "You must accept the terms and conditions.")
            return redirect('register')

        # Save user
        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=make_password(password1),
            dob=parse_date(dob),
            gender=gender,
            marital_status=marital_status,
            agree_to_terms=True if terms == 'on' else False,
        )

        # print(f"""
        # User registration details:
        # Username: {username}
        # Email: {email}
        # Password: {password1}
        # confirm Password: {password2}
        # dob: {dob}
        # gender: {gender}
        # marital_status: {marital_status}
        # agree_to_terms: {terms}
        # """)

        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'register.html')


@login_required(login_url='login')
@never_cache
def home_view(request):
    return render(request, 'home.html')

@login_required
def update_bio(request):
    user = request.user
    if request.method == 'POST':
        form = UserBioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Bio updated successfully.")
            return redirect('home')  # or change to 'profile' if you have one
    else:
        form = UserBioForm(instance=user)

    return render(request, 'update_bio.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def soft_delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_deleted = True
    user.save()
    return redirect('admin:web_app_customuser_changelist')


# ================= Custom Admin Panel ==================

def is_admin(user):
    return user.is_staff and user.is_superuser


@csrf_protect
@never_cache
def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            request.session['admin_id'] = user.id
            login(request, user)  # Ensure admin is logged in
            # Add feedback
            messages.success(request, "Admin login successful.")
            # Ensure this matches your urls.py
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin.')

    return render(request, 'admin-panel/admin_login.html')  # Fix template path


@never_cache
@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    users = CustomUser.objects.filter(is_deleted=False)

    # Get filters
    search = request.GET.get('search', '')
    gender = request.GET.get('gender', '')
    marital_status = request.GET.get('marital_status', '')
    is_active = request.GET.get('is_active', '')
    is_staff = request.GET.get('is_staff', '')
    is_superuser = request.GET.get('is_superuser', '')
    ordering = request.GET.get('ordering', '-date_joined')  # Default newest

    # Apply filters
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(gender__icontains=search)
        )
    if gender:
        users = users.filter(gender=gender)
    if marital_status:
        users = users.filter(marital_status=marital_status)
    if is_active:
        users = users.filter(is_active=(is_active == "Yes"))
    if is_staff:
        users = users.filter(is_staff=(is_staff == "Yes"))
    if is_superuser:
        users = users.filter(is_superuser=(is_superuser == "Yes"))

    # Ordering
    users = users.order_by(ordering)

    # Pagination
    paginator = Paginator(users, 10)  # 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'filters': {
            'search': search,
            'gender': gender,
            'marital_status': marital_status,
            'is_active': is_active,
            'is_staff': is_staff,
            'is_superuser': is_superuser,
            'ordering': ordering,
        }
    }

    return render(request, 'admin-panel/admin_dash.html', context)


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')
        is_active = bool(request.POST.get('is_active'))
        is_staff = bool(request.POST.get('is_staff'))
        is_superuser = bool(request.POST.get('is_superuser'))

        # Server-side validations
        if not username or not email or not password or not confirm_password:
            messages.error(request, "All required fields must be filled.")
            return redirect('admin_create_user')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('admin_create_user')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('admin_create_user')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('admin_create_user')

        user = CustomUser(
            username=username,
            email=email,
            password=make_password(password),
            dob=dob,
            gender=gender,
            marital_status=marital_status,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        user.save()
        messages.success(request, "User created successfully.")
        return redirect('admin_dashboard')

    return render(request, 'admin-panel/admin_create_user.html')


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id, is_deleted=False)

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        dob = request.POST.get('dob') or None
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')

        # Server-side validations
        if not username or not email:
            messages.error(request, "Username and email are required.")
            return redirect('admin_edit_user', user_id=user.id)

        # Check unique constraints only if values changed
        if username != user.username and CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('admin_edit_user', user_id=user.id)

        if email != user.email and CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('admin_edit_user', user_id=user.id)

        user.username = username
        user.email = email
        user.dob = dob
        user.gender = gender
        user.marital_status = marital_status
        user.is_active = bool(request.POST.get('is_active'))
        user.is_staff = bool(request.POST.get('is_staff'))
        user.is_superuser = bool(request.POST.get('is_superuser'))

        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('admin_dashboard')

    return render(request, 'admin-panel/admin_edit_user.html', {'user': user})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_soft_delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_deleted = True
    user.save()
    messages.success(request, "User soft-deleted")
    return redirect('admin_dashboard')


def admin_logout_view(request):
    logout(request)
    messages.success(request, "Admin logged out")
    return redirect('admin_login')
