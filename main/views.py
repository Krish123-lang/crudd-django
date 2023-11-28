from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post
# Create your views here.


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
