from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Document
from .forms import RegisterForm, DocumentForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    """User's dashboard showing uploaded documents."""
    documents = Document.objects.filter(user=request.user)
    return render(request, 'users/dashboard.html', {'documents': documents})

def upload_document(request, unique_url):
    """
    Customer upload page.
    Any customer can upload a file using a unique user-specific URL.
    The file is automatically linked to that user.
    """
    user = get_object_or_404(CustomUser, unique_url=unique_url)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = user
            document.save()
            return render(request, 'users/upload_success.html', {'user': user})

    else:
        form = DocumentForm()

    return render(request, 'users/upload.html', {'form': form, 'user': user})
