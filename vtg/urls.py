from django.urls import path
from . import views
urlpatterns=[path('',views.hom, name='hom'), path('location',views.location,name="location")]
