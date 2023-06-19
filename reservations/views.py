from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from .models import Room
from .models import Reservation
import datetime


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
        return redirect("/rooms/")


class ModifyRoom(View):
    def get(self, request, room_id):
        context = {'room': Room.objects.get(id=room_id)}
        return render(request, 'modify_room.html', context=context)

    def post(self, request, room_id):
        # get input data
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        projector = request.POST.get('projector')
        room = Room.objects.get(id=room_id)

        # validate name
        if name != room.name and name in [r.name for r in Room.objects.all()]:
            context = {
                'room': room,
                'message': f"Room {name} already exists!"
            }
            return render(request, 'modify_room.html', context=context)

        # validate capacity
        if not isinstance(capacity, int) or capacity < 0:
            context = {
                'room': room,
                'message': "Room capacity must be positive integer!"
            }
            return render(request, 'modify_room.html', context=context)

        # edit room data
        room.name = name
        room.capacity = capacity
        room.projector_availability = projector
        room.save()
        return redirect("/rooms/")


class ReserveRoom(View):
    def get(self, request, room_id):
        context = {'room': Room.objects.get(id=room_id)}
        return render(request, 'reservation.html', context=context)

    def post(self, request, room_id):
        # get input data
        room = Room.objects.get(id=room_id)
        reservation_date = request.POST.get('date')
        comment = request.POST.get('comment')

        # validate if reserved
        if Reservation.objects.filter(room=room, date=reservation_date):
            context = {
                'room': room,
                'message': "This room has already been reserved!"
            }
            return render(request, 'reservation.html', context=context)

        # validate past date
        if reservation_date < str(datetime.date.today()):
            context = {
                'room': room,
                'message': "Past date is not a valid option."
            }
            return render(request, 'reservation.html', context=context)

        # create object
        Reservation.objects.create(room=room, date=reservation_date, comment=comment)
        return redirect("/rooms/")
