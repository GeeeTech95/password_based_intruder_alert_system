from django.urls import path
from . import views


urlpatterns = [

    path("",views.Index.as_view(),name = "index"),
    path("login/",views.Login.as_view(),name = "login"),
    path("logout/",views.Logout.as_view(),name = "logout"),
    path("resource/",views.Resource.as_view(),name = "resource")

  
]