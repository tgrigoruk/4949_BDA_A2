from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from pages.services import get_prediction


def home(request):
    return render(request, "home.html")


def survey(request):
    ranking_questions = [
        "Online boarding",
        "Inflight wifi service",
        "Seat comfort",
        "Inflight entertainment",
        "Leg room service",
        "On-board service",
    ]
    return render(
        request,
        "survey.html",
        {
            "questions": ranking_questions,
            "numbers": [i for i in range(0, 6)],
        },
    )


def submit(request):

    try:
        data = {
            "Age": int(request.POST["age"]),
            "Type of Travel": request.POST["Type of Travel"],
            "Class": request.POST["Class"],
            "Online boarding": int(request.POST["Online boarding"][0]),
            "Inflight wifi service": int(request.POST["Inflight wifi service"][0]),
            "Seat comfort": int(request.POST["Seat comfort"][0]),
            "Inflight entertainment": int(request.POST["Inflight entertainment"][0]),
            "Leg room service": int(request.POST["Leg room service"][0]),
            "On-board service": int(request.POST["On-board service"][0]),
        }
        prediction = get_prediction(data)

    except:
        return render(
            request,
            "home.html",
            {"errorMessage": "Bad or missing values in form - please try again."},
        )
    else:
        return HttpResponseRedirect(
            reverse("results", kwargs={"prediction": prediction})
        )


def results(request, prediction):
    return render(request, "results.html", {"is_satisfied": prediction == 1})


def about(request):

    images = [
        "https://i.ibb.co/RvTJMbp/histogram-Class.png",
        "https://i.ibb.co/hVNvCYk/histogram-Type-of-Travel.png",
        "https://i.ibb.co/nmvb1xs/histogram-Age.png",
        "https://i.ibb.co/LzKf29Y/histogram-Inflight-entertainment.png",
        "https://i.ibb.co/0hQ9Rgg/histogram-Inflight-wifi-service.png",
        "https://i.ibb.co/S3RGZ4K/histogram-Leg-room-service.png",
        "https://i.ibb.co/jJjcrFT/histogram-On-board-service.png",
        "https://i.ibb.co/HYMN4Hc/histogram-Online-boarding.png",
        "https://i.ibb.co/r0z4VNk/histogram-Seat-comfort.png",
    ]
    return render(
        request,
        "about.html",
        {"images": images},
    )
