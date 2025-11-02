from django.urls import path
from .views import search_view, autocomplete_view

app_name = 'search'

urlpatterns = [
    path('', search_view, name='search'),
    path('autocomplete/', autocomplete_view, name='autocomplete'),
]
