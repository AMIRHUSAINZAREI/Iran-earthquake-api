from django.urls import path
from .views import sample_view


urlpatterns = [
        path('', sample_view),
]
