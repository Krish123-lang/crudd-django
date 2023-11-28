# Login, Register

1. > `pip3 install crispy-bootstrap5`
2. >  `pip install django-crispy-forms`
3. >  `python3 manage.py startapp main`
4. >  `settings.py`
```
INSTALLED_APPS = [
    "main",
    "crispy_forms",
    "crispy_bootstrap5",
    ...
]

CRISPY_ALLOWED_TEMPLATE_PACK = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
```
5. >  `urls.py(project)`
```
from django.urls import path, include

urlpatterns = [
    path("", include('main.urls')),
    path("", include("django.contrib.auth.urls")),
]
```
6. >  `forms.py`
```
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ["username","firstname","lastname", "email", "password1", "password2"]
```
7. >  `urls.py(main)`
```
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sign-up", views.sign_up, name="sign_up"),
]
```
8. >  `views.py`
```
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def home(request):
    return render(request, "main/home.html")

def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, "registration/sign_up.html", context)
```
9. >  `base.html`
```
<title>Mysite | {% block title %}{% endblock title %}</title>
<ul class="navbar-nav">
    <li class="nav-item">
        <a href="{% url "home" %}" class="nav-link">Home</a>
    </li>
    <li class="nav-item">
        <a href="{% url "create_post" %}" class="nav-link">Post</a>
    </li>
</ul>

<ul class="navbar-nav">
    {% if user.is_authenticated %}
        <span class="navbar-text">{{user.username}} | </span>
        <li class="nav-item">
            <a href="{% url "logout" %}" class="nav-link">Logout</a>
        </li>
    {% else %}
        <li class="nav-item">
            <a href="{% url "login" %}" class="nav-link">Login</a>
        </li>
    {% endif %}
</ul>

<div class="container mt-3 mb-3">
    {% block content %}{% endblock content %}
</div>
```
10. >  Create `templates/main/home.html`, `templates/registration/login.html`, `templates/main/sign_up.html`, 
11. >  `registration/login.html`
```
{% extends "base.html" %}
{% block title %}Login{% endblock title %}
{% block content %}
    {% load crispy_forms_tags %}
    <form action="" method="post">
        {% csrf_token %}
        {{form|crispy}}
        <p>Don't have an account? <a href="{% url "sign_up" %}">Register</a></p>
        <button type="submit" class="btn btn-success">Login</button>
    </form>
{% endblock content %}
```
12. >  `registration/sign_up.html`
```
{% extends "base.html" %}
{% block title %}Sign Up{% endblock title %}
{% block content %}
    {% load crispy_forms_tags %}
    <form action="" method="post">
        {% csrf_token %}
        {{form|crispy}}
        <p>Already have an account? <a href="{% url "login" %}">Login</a></p>
        <button type="submit" class="btn btn-success">Sign Up</button>
    </form>
{% endblock content %}
```
---
# Showing Posts
> 1. `models.py`
```
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description
```
> 2. `admin.py`
```
from django.contrib import admin
from .models import Post
admin.site.register(Post)
```
> 3. `forms.py`
```
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=50)
    lastname = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ["username", "firstname", "lastname", "email", "password1", "password2"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]
```
> 4. `urls.py(main)`
```
urlpatterns = [
    ...
    path("create-post", views.create_post, name="create_post"),
]
```
> 5. `views.py`
```
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post

@login_required(login_url="login")
def home(request):
    posts = Post.objects.all()
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
    context = {'posts': posts}
    return render(request, "main/home.html", context)
...

@login_required(login_url="login")
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, "main/create_post.html", context)
```
> 6. `main/create_post.html`
```
{% extends "base.html" %}
{% block title %}Create Post{% endblock title %}

{% block content %}
    {% load crispy_forms_tags %}
    <form action="" method="POST">
        {% csrf_token %}
        {{form|crispy}}
        <button type="submit" class="btn btn-success">Post</button>
    </form>
{% endblock content %}
```
> 7. `main/home.html`
```
{% extends "base.html" %}
{% block title %}Home{% endblock title %}

{% block content %}
<h1>Home</h1>
{% for post in posts %}
<div class="card mt-2">
    <div class="card-header"><strong>@{{post.author}}</strong></div>
    <div class="card-body d-flex flex-row justify-content-between">
        <div>
            <h5 class="card-title"> {{post.title}} </h5>
            <p> {{post.description}} </p>
        </div>
        <div>
            {% if user == post.author %}
            <form action="" method="POST">
                {% csrf_token %}
                <button type="submit" name="post-id" value="{{post.id}}" class="btn btn-danger">Delete</button>
            </form>
            {% endif %}
        </div>
    </div>
    <div class="card-footer text-muted"> {{post.created_at}} </div>
</div>
{% empty %}
<p>No posts yet</p>
{% endfor %}
{% endblock content %}
```
---