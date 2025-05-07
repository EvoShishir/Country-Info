from django.urls import path
from .views import (
    CountryListView,
    CountryDetailView,
    CreateCountryView,
    UpdateCountryView,
    DeleteCountryView,
    RegionalCountryListView,
    SameLanguageCountryListView,
    SearchCountryView,
)

urlpatterns = [
    path("countries", CountryListView.as_view()),
    path("countries/<int:pk>", CountryDetailView.as_view()),
    path("countries/create", CreateCountryView.as_view()),
    path("countries/update/<int:pk>", UpdateCountryView.as_view()),
    path("countries/delete/<int:pk>", DeleteCountryView.as_view()),
    path("countries/<int:pk>/regional-countries", RegionalCountryListView.as_view()),
    path("countries/<int:pk>/same-language", SameLanguageCountryListView.as_view()),
    path("countries/search/", SearchCountryView.as_view()),
]
