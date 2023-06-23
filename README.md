# Conference room rental app #

***

### Features: ###

1. Conference room booking: You can view available conference rooms and book them for specific dates.
2. Room availability management: You can add, edit, and delete conference rooms.
3. Search and filtering: You can search for available conference rooms based on criteria like capacity and projector
   availability.
4. Database: By default, the application uses SQLite as the database. You can change the database configuration in the
   settings.py file.

### Prerequisites ###

Python 3.x  
Django 4.x

### How to run ###

1. Clone the repository to your local machine.
   ```git clone https://github.com/saradonin/conference_room_rental```
2. Install the required dependencies:
   ```pip install -r requirements.txt```
3. Set up the database
   ```python manage.py migrate```
   Run developement server
3. ```python manage.py runserver```
4. Access the application in your web browser at `http://127.0.0.1:8000/` or `http://localhost:8000/`

