from django.urls import path 
# from django.http import HttpResponse
from . import views 

# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='my_view'),
    path('stream/', views.stream_view, name='stream'),
    path('jamming/', views.jamming, name='jamming')
]
