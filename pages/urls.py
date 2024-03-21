from django.urls import path

from .views import (aboutPageView, homePageView, homePost, results,
                    terencePageView, todos)

urlpatterns = [
    path("", homePageView, name="home"),
    path("about/", aboutPageView, name="about"),
    path("terence/", terencePageView, name="terence"),
    path("homePost/", homePost, name="homePost"),
    path("results/<int:choice>/<str:gmat>", results, name="results"),
    path("todos/", todos, name="todos"),
]
