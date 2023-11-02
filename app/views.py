from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from authentication.models import User
from authentication.models import Notification

def AboutView(request):
    return render(request,'about.html')


def contacts(request):
    return render(request,'contact.html')

def frequentlyaskedquestions(request):
    return render(request,'python-programming-help-services/frequently_asked_questions.html')

def policy(request):
    return render(request,'policy.html')