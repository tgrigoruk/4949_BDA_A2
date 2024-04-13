from django.urls import path

from .views import home, submit, about, survey, results

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("survey/", survey, name="survey"),
    path("submit/", submit, name="submit"),
    path("results/<int:prediction>", results, name="results"),
]
