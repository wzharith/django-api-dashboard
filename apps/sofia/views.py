from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import template


def index(request):
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))
