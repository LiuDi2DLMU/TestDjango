from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    return render(request, 'neuropeptide/index.html')


def main(request):
    return redirect("/main/")
