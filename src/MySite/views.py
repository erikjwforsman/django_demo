from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from operator import attrgetter

from account.forms import RegistrationForm,AccountAuthenticationForm

from recipe.models import Comment

def home_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        login_form=AccountAuthenticationForm(request.POST)#
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get("username")
            raw_password=form.cleaned_data.get("password1")
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect("home")
        #elif toinen on validi
        elif login_form.is_valid():
            username=request.POST["username"]
            password=request.POST["password"]
            user=authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")


        else:
            context["registration_form"] = form


    else:
        user=request.user
        kommentti_lista = Comment.objects.filter(recipe_commented__author__username=user.username)
        kommentti_lista =sorted(kommentti_lista, key=attrgetter("create_date"), reverse=True)
        kommentti_lista=kommentti_lista[0:5]
        context["kommentti_lista"]=kommentti_lista
        login_form = AccountAuthenticationForm()#
        form = RegistrationForm()
        context["registration_form"]=form
        context["login_form"]=login_form



    return render(request, "index.html", context)
