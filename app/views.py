from django.shortcuts import redirect, render
from requests import delete

# Create your views here.
from .forms import BlogForm
from .models import Blog
from django.contrib import messages
from django.contrib.auth.decorators import  login_required


def home(request):
    blogs = Blog.objects.all()
    context = {"blogs": blogs}
    return render(request, "app/home.html", context)

@login_required
def add(request):
    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created Successfully !")
            return redirect("home")
    context = {"form": form}
    return render(request, "app/add.html", context)


def read(request, pk):
    reads = Blog.objects.get(id=pk)
    context = {"reads": reads}
    return render(request, "app/read.html", context)

@login_required
def update(request, pk):
    upblog = Blog.objects.get(id=pk)
    form = BlogForm(instance=upblog)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=upblog)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfully !")
            return redirect("home")
    context = {"form": form, "upblog": upblog}
    return render(request, "app/add.html", context)

@login_required
def delete(request, pk):
    delblog = Blog.objects.get(id=pk)
    if request.method == "POST":
        delblog.delete()
        messages.success(request, "Deleted Successfully !")
        return redirect("home")
    context = {"delblog": delblog}
    return render(request, "app/delete.html", context)
