from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View


def home(request):
    return render(request, 'home.html')


class AddRoom(View):
    def get(self, request):
        return render(request, 'add_room.html')
    def post(self, request):
        return redirect('/home/')