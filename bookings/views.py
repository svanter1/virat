from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'index.html')
def newpay(request):
    return render(request, 'newpay1.html')