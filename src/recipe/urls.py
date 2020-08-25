from django.urls import path
from . import views

app_name = "recipe"

urlpatterns = [
    path("lisaa/", views.add_recipe_view, name="add"),
    path("kategoria/<dish>/", views.recipes_view, name="recipes"),
    path("selaa/", views.recipes_view, name="recipes"),
    #path("selaa/<slug:slug>/", views.single_recipe_view, name="single"),
    path("selaa/<slug>/", views.single_recipe_view, name="single"),
    path("muokkaa/<slug>/", views.edit_recipe_view, name="edit"),
    path("poista/<id>/", views.delete_recipe_view, name="delete"),
]
