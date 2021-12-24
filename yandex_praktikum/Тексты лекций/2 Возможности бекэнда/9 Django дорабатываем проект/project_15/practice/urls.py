from django.urls import path

from . import views

urlpatterns = [
    path("thank-you/", views.thankyou, name="thankyou"),
    path("", views.index, name="index"),
]
