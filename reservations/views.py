from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from .models import Room


def home(request):
    return render(request, 'home.html')


class AddRoom(View):
    def get(self, request):
        return render(request, 'add_room.html')

    def post(self, request):
        # get input data
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector = request.POST.get('projector')

        # validate data
        if name in [room.name for room in Room.objects.all()]:
            message = f"Room {name} already exists!"
        elif not isinstance(capacity, int) or capacity < 0:
            message = f"Room capacity must be positive integer!"
        else:
            # add room to database
            Room.objects.create(name=name, capacity=capacity, projector_availability=projector)
            message = f"Room {name} added successfully!"

        return render(request, 'add_room.html', context={'message': message})


class RoomList(View):
    def get(self, request):
        context = {
            'rooms': Room.objects.all().order_by("name")
        }
        return render(request, 'room_list.html', context=context)


class DeleteRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        room.delete()
        context = {
            'rooms': Room.objects.all().order_by("name")
        }
        return render(request, 'room_list.html', context=context)


class ModifyRoom(View):
    def get(self, request, room_id):
        context = {'room': Room.objects.get(id=room_id)}
        return render(request, 'modify_room.html', context=context)

    def post(self, request, room_id):
        # get input data
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector = request.POST.get('projector')

        # validate data
        if name in [room.name for room in Room.objects.all()]:
            message = f"Room {name} already exists!"
            return render(request, 'modify_room.html', {'message': message, })
        elif not isinstance(capacity, int) or capacity < 0:
            message = f"Room capacity must be positive integer!"
            return render(request, 'modify_room.html', {'message': message, })
        else:
            room = Room.objects.get(id=room_id)
            room.name = name
            room.capacity = capacity
            room.projector_availability = projector
            room.save()

        context = {'rooms': Room.objects.all().order_by("name")}
        return render(request, 'room_list.html', context=context)
