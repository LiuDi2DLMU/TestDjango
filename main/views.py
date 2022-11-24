from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return render(request, 'main/index.html')


def neuropepetide(request):
    return HttpResponseRedirect(reverse('neuropeptide:index'))


def zsm(request):
    return HttpResponseRedirect(reverse('zsm:index'))
