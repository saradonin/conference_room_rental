from django.db import models


class Room(models.Model):
    """
    Represents a room with a name, capacity, and projector availability.
    """
    name = models.CharField(max_length=255, unique=True)
    capacity = models.PositiveIntegerField()
    projector_availability = models.BooleanField(default=False)


class Reservation(models.Model):
    """
    Represents a reservation made for a specific room on a specific date.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('room', 'date')
