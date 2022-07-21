from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name='add'),
    path('random/', views.random, name='random'),
    path('wiki/<str:title>', views.wiki, name='wiki'),
    path('wiki/<str:title>/edit/', views.edit, name='edit'),
    path('save/', views.save, name='save'),
    path('/search', views.search, name='search')
]
