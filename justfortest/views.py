from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse


def index(request):
    return render(request, "justfortest/mega_start.html")

def under60(request):
    return render(request,"justfortest/mega_under50.html")

def over60(request):
    return render(request,"justfortest/mega_over50.html")


def get_prediction(request):
    return JsonResponse({"prediction": "under"})

