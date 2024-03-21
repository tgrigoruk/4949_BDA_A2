# pages/views.py
from django.http import Http404
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from pages.models import Item, ToDoList

from .forms import RegisterForm


def register(response):
    # Handle POST request.
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            return redirect("../")  # Go to home page
    # Handle GET request.
    else:
        form = RegisterForm()
    return render(response, "registration/register.html", {"form": form})


def homePageView(request):
    # return request object and specify page.
    return render(
        request,
        "home.html",
        {
            "mynumbers": [i for i in range(1, 11)],
            "firstName": "Terence",
            "lastName": "Grigoruk",
        },
    )


def aboutPageView(request):
    # return request object and specify page.
    return render(request, "about.html")


def terencePageView(request):
    # return request object and specify page.
    return render(request, "terence.html")


def todos(request):
    items = Item.objects
    itemErrandDetail = items.select_related("todolist")
    print(itemErrandDetail[0].todolist.name)
    return render(request, "todos.html", {"todos": itemErrandDetail})


def homePost(request):
    # Create variable to store choice that is recognized through entire function.
    choice = None
    gmat = None

    try:
        # Extract value from request object by control name.
        currentChoice = request.POST["choice"]
        gmatStr = request.POST["gmat"]

        # Crude debugging effort.
        print("*** Years work experience: " + str(currentChoice))
        choice = int(currentChoice)
        gmat = float(gmatStr)

    # Enters 'except' block if integer cannot be created.
    except:
        return render(
            request,
            "home.html",
            {
                "errorMessage": "*** The choice was missing please try again",
                "mynumbers": [i for i in range(1, 11)],
            },
        )
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse(
                "results",
                kwargs={"choice": choice, "gmat": gmat},
            )
        )


import pickle

import pandas as pd
import sklearn


def results(request, choice, gmat):
    print("*** Inside reults()")
    # load saved model
    with open("../model_pkl", "rb") as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSampleDf = pd.DataFrame(columns=["gmat", "work_experience"])

    workExperience = float(choice)
    print("*** GMAT Score: " + str(gmat))
    print("*** Years experience: " + str(workExperience))
    singleSampleDf = singleSampleDf._append(
        {"gmat": gmat, "work_experience": workExperience}, ignore_index=True
    )

    singlePrediction = loadedModel.predict(singleSampleDf)

    print("Single prediction: " + str(singlePrediction))
