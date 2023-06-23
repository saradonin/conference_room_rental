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
        projector = False if not projector else True

        # validate data
        if Room.objects.filter(name=name).exists():
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
        rooms = Room.objects.all().order_by("name")
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = datetime.date.today() in reservation_dates
        return render(request, 'room_list.html', context={'rooms': rooms})


class DeleteRoom(View):
    def get(self, request, room_id):
        context = {'room': Room.objects.get(id=room_id)}
        return render(request, 'delete_room_confirmation.html', context=context)

    def post(self, request, room_id):
        confirm = request.POST.get('confirm')
        room = Room.objects.get(id=room_id)
        if confirm == "Yes":
            room.delete()
            return redirect("/rooms/")
        else:
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
        projector = request.POST.get('projector')
        projector = False if not projector else True
        room = Room.objects.get(id=room_id)

        # validate name
        if name != room.name and Room.objects.filter(name=name).exists():
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
        room = Room.objects.get(id=room_id)
        reservations = room.reservation_set.filter(room=room_id, date__gte=str(datetime.date.today())).order_by('date')
        context = {'room': room,
                   'reservations': reservations
                   }
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


class RoomDetails(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        reservations = room.reservation_set.filter(room=room_id, date__gte=str(datetime.date.today())).order_by('date')
        context = {
            'room': room,
            'reservations': reservations,
        }
        return render(request, 'room_details.html', context=context)


class SearchRoom(View):
    def get(self, request):
        min_capacity = request.GET.get('capacity')
        min_capacity = int(min_capacity) if min_capacity else 0
        projector = request.GET.get('projector')
        projector = True if projector else False
        rooms = Room.objects.all()
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = datetime.date.today() in reservation_dates
        context = {
            'rooms': Room.objects.filter(capacity__gte=min_capacity, projector_availability=projector)
        }
        return render(request, 'search_room.html', context=context)
