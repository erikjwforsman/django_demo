from django.urls import path
from . import views

app_name = "account"

urlpatterns= [
    path("user/", views.user_view, name="user"),
    path("user/<int:pk>/", views.user_view, name="user_pk"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.registration_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("must_authenticate/", views.must_authenticate_view, name="must_authenticate"),
    path("update", views.update_view, name="update"),

]
