from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "justfortest/mega_under50.html")


