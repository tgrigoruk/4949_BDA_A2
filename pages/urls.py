from django.urls import path, include

from .views import (
    aboutPageView,
    homePageView,
    homePost,
    logoutView,
    message,
    register,
    results,
    secretArea,
    terencePageView,
    todos,
)

urlpatterns = [
    path("", homePageView, name="home"),
    path("about/", aboutPageView, name="about"),
    path("terence/", terencePageView, name="terence"),
    path("homePost/", homePost, name="homePost"),
    path("results/<int:choice>/<str:gmat>", results, name="results"),
    path("todos/", todos, name="todos"),
    path("register/", register, name="register"),
    path("message/<str:msg>/<str:title>/", message, name="message"),
    path("", include("django.contrib.auth.urls")),
]
