from django.urls import path, re_path
from . import views

urlpatterns = [
    path('all/', views.all_earthquakes),
    path('last/<int:n>/', views.last_n_earthquake),
    re_path(r'magnitude_gte/(?P<m>\d+\.\d{1})/', views.magnitude_gte),
    path('magnitude_gte/<int:m>/', views.magnitude_gte),
]
