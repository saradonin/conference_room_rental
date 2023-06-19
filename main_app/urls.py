"""
URL configuration for main_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reservations.views import home
from reservations.views import AddRoom
from reservations.views import RoomList
from reservations.views import DeleteRoom


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
    path('room/new/', AddRoom.as_view()),
    path('rooms/', RoomList.as_view()),
    path('room/delete/<int:id>/', DeleteRoom.as_view()),
]
