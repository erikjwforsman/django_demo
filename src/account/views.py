from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm,AccountAuthenticationForm, AccountUpdateForm
from operator import attrgetter
from recipe.filters import OhjeFilter

from django import forms
from account.models import Account
from recipe.models import Ohje, Comment
# Create your views here.
def user_view(request, pk=None):

    if pk:
        user=get_object_or_404(Account, pk=pk)
    else:
        user=request.user

    context = {}
    #resepti_lista=sorted(Ohje.objects.filter(author=user), key=attrgetter("date_published"), reverse=True)

    resepti_lista=Ohje.objects.filter(author=user)
    myFilter = OhjeFilter(request.GET, queryset=resepti_lista)
    resepti_lista = myFilter.qs
    resepti_lista=sorted(resepti_lista, key=attrgetter("date_published"), reverse=True)
    ###
    #user=request.user
    #if user is request.user:
    kommentti_lista = Comment.objects.filter(recipe_commented__author__username=user.username)
    kommentti_lista =sorted(kommentti_lista, key=attrgetter("create_date"), reverse=True)
    context["kommentti_lista"]=kommentti_lista
    ###

    context["resepti_lista"]=resepti_lista
    context["user"]=user
    context["myFilter"]=myFilter
    return render(request, "account/user.html", context) #vaihda user.html testin tilalle

def logout_view(request):
    logout(request)
    return redirect("home")

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get("username")
            raw_password=form.cleaned_data.get("password1")
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect("home")
        else:
            context["registration_form"] = form
    else:
        form = RegistrationForm()
        context["registration_form"]=form
    return render(request, "account/register.html", context)

def login_view(request):
    context = {}

    user=request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form=AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username=request.POST["username"]
            password=request.POST["password"]
            user=authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")
    else:
        form = AccountAuthenticationForm()

    context["login_form"]=form
    return render(request, "account/login.html", context)

def update_view(request):
    if not request.user.is_authenticated: #Saattaa olla virhe
        return redirect("home")

    context = {}

    if request.POST:
        form=AccountUpdateForm(request.POST, request.FILES or None, instance=request.user)#Tänne lisäys
        if form.is_valid():
            form.save()
            #return render(request, "account/user.html", {})
    else:
        form = AccountUpdateForm(
            initial={
                "first_name":request.user.first_name,
                "last_name":request.user.last_name,
                "username":request.user.username,
                "email":request.user.email,
                "motto":request.user.motto,
                "image": request.user.image,
            }
        )

    context["account_form"]=form
    #Saatetaan vielä lisätä jonkinlainen resepti lista
    return render(request, "account/update.html", context)

def must_authenticate_view(request):
    return render(request, "account/must_authenticate.html", {})
