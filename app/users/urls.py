from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("create/", views.CreateUserApiView.as_view(), name="create"),
]