from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
from .models import New


class HomePageView(ListView):
    model = New
    template_name = 'home.html'
    context_object_name = 'news_list'