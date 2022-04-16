from django.urls import path
from . import views


urlpatterns = [
    path("search/", views.search, name="search"),
    path("loadData/", views.loadData, name="loadData"),
    path("saveSearch/", views.saveSearch, name="saveSearch"),
    path("checkPrice/", views.checkPrice, name="checkPrice"),
    path("deleteSearch/", views.deleteSearch, name="deleteSearch")
]