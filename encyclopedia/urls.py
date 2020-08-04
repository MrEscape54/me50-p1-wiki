from django.urls import path

from encyclopedia import views

app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("create/", views.new_entry, name="new_entry"),
    path("edit/<str:title>/", views.edit_entry, name="edit_entry"),
    path("random/", views.random_page, name="random"),
]
