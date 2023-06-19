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
from reservations.views import ModifyRoom
from reservations.views import Reservation



urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
    path('room/new/', AddRoom.as_view()),
    path('rooms/', RoomList.as_view()),
    path('room/delete/<int:room_id>/', DeleteRoom.as_view()),
    path('room/modify/<int:room_id>/', ModifyRoom.as_view()),
    path('room/reserve/<int:room_id>', Reservation.as_view()),
]
