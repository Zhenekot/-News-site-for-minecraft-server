from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
from .models import New


class HomePageView(ListView):
    template_name = 'home.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        return New.objects.filter(is_archived=False).order_by('-date_of_create')[:4]


class NewPageView(ListView):
    template_name = 'newpage.html'
    context_object_name = 'news_list'
    paginate_by = 8
    def get_queryset(self):
        return New.objects.filter(is_archived=False)