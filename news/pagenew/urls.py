
from . import views
from django.urls import path, include
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('news/', views.NewPageView.as_view(), name='new'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('news/<int:pk>/', views.NewDetailView.as_view(), name='news_detail'),

]