#!/usr/bin/python3
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request handlers


def say_hello(request):
    return HttpResponse('hello')
