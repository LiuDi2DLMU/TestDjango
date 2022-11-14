from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello world ! ")


def first(request):
    context          = {}
    context['hello'] = 'Hello World, first!'
    return render(request, 'first.html', context)
    
def index(request):
    return HttpResponse("Index! ")
