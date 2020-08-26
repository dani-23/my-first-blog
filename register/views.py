from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form =  RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            return redirect("post_list")
    else: 
        form =  RegisterForm()
    return render(request, "register/register.html", {"form":form})