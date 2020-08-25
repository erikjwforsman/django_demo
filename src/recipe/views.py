from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from account.forms import RegistrationForm,AccountAuthenticationForm
from operator import attrgetter
from .filters import OhjeFilter

from account.models import Account
from recipe.models import Ohje, Comment
from recipe.forms import AddRecipeForm, AddCommentForm, UpdateRecipeForm


# Create your views here.
def add_recipe_view(request):
    context = {}
    user=request.user

    if not user.is_authenticated:
        return redirect("home")

    form = AddRecipeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(username=user.username).first()
        obj.author=author
        obj.save()
        form=AddRecipeForm()

    context["form"]=AddRecipeForm()
    return render(request, "recipe/add_recipe.html", context)

def recipes_view(request, dish=None):
    context = {}
    if dish is None:
        resepti_lista=Ohje.objects.all()
    else:
        resepti_lista = Ohje.objects.filter(dish=dish)


    myFilter = OhjeFilter(request.GET, queryset=resepti_lista)
    resepti_lista = myFilter.qs

    resepti_lista=sorted(resepti_lista, key=attrgetter("date_published"), reverse=True)


    if request.POST:
        form = RegistrationForm(request.POST)
        login_form=AccountAuthenticationForm(request.POST)#
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get("username")
            raw_password=form.cleaned_data.get("password1")
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect("recipe:recipes")

        elif login_form.is_valid():
            username=request.POST["username"]
            password=request.POST["password"]
            user=authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("recipe:recipes")

        else:
            context["registration_form"] = form


    else:
        user=request.user
        kommentti_lista = Comment.objects.filter(recipe_commented__author__username=user.username)
        kommentti_lista =sorted(kommentti_lista, key=attrgetter("create_date"), reverse=True)
        context["kommentti_lista"]=kommentti_lista


        login_form = AccountAuthenticationForm()#
        form = RegistrationForm()
        context["registration_form"]=form
        context["login_form"]=login_form
        context["resepti_lista"]=resepti_lista
        context["myFilter"]=myFilter

        return render(request, "recipe/recipes.html", context)

def single_recipe_view(request, slug):
    user=request.user #Toimii

    context = {}
    resepti_lista = get_object_or_404(Ohje, slug=slug)
    #####
    form = AddCommentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.recipe_commented=resepti_lista
        #if user.is_authenticated:
        #    obj.author=author
        obj.save()
        if user.is_authenticated:
            form=AddCommentForm(initial={'author': user.username})
        else:
            form=AddCommentForm(initial={'author': "Vieras"})

    if user.is_authenticated:
        context["form"]=AddCommentForm(initial={'author': user.username})
    else:
        context["form"]=AddCommentForm(initial={'author': "Vieras"})

    #####
    #####Ongelmakohta filtteröinti#####
    kommentti_lista = Comment.objects.filter(recipe_commented=resepti_lista)
    #####
    context["kommentti_lista"]=kommentti_lista

    context["resepti_lista"]=resepti_lista
    return render(request, "recipe/single_recipe.html", context)

def edit_recipe_view(request, slug):
    context={}

    user=request.user


    if not user.is_authenticated:
        return redirect("home")


    ohje = get_object_or_404(Ohje, slug=slug)

    if ohje.author != user:
        return redirect("home")

    if request.POST:
        form=UpdateRecipeForm(request.POST or None, request.FILES or None, instance=ohje)

        if form.is_valid():
            obj=form.save(commit=False)
            obj.save()
            ohje=obj

    form=UpdateRecipeForm(initial={
        "title": ohje.title,
        "dish": ohje.dish,
        "cooking_time": ohje.cooking_time,
        "ingredients": ohje.ingredients,
        "body": ohje.body,
        "image": ohje.image,
    })
    context["form"]=form
    context["ohje"]=ohje
    return render(request, "recipe/edit_recipe.html", context)

def delete_recipe_view(request, id):
    context={}
    poistettava=get_object_or_404(Ohje, id=id)


    if request.POST:
        if request.user.is_authenticated and request.user.username == poistettava.author.username:
            poistettava.delete()
            return redirect("account:user")
        else:
            return redirect("home")
    context["poistettava"]=poistettava
    return render(request, "recipe/delete_recipe.html", context)
