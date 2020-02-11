# django3_asgi

This is a test project of how to implement WebSockets with Django >= 3.0 without the need for any extra libraries:

_NOTE:_ Require Python 3.6 or higher

## How test it:

### 1. Create a folder, clone the repo, create a virualenv and install the required packages:

```bash
mkdir django_websockets && cd django_websockets
python -m venv venv
source venv/bin/activate
git clone https://github.com/eamigo86/django3_asgi && cd django3_asgi
pip install -r requirements.txt
```

### 2. Run Django migrations, create a superuser, and collect the static files (optional for admin only):

```bash
./manage.py migrate
./manage.py createsuperuser
./manage.py collectstatic
```

### 3. Run the server, navigate to your admin enpoint and create some Car objects:

```bash
uvicorn --port 8000 websocket_app.asgi:application --reload
```

### 4. Open a new browser tab and in Developer Tools, go to Console tab go test the websocket conection:

```javascript
ws = new WebSocket("ws://localhost:8000/");
ws.onmessage = event => console.log(event.data);

// Send some message to the websocket server
ws.send("ping"); // recieve "pong!"

ws.send("car"); // recieve the plate value for the first car object in db
ws.send("car:3"); // recieve the plate value for the car with id=3 in your db
ws.send("car:invalid_id"); // recieve "Do not exists any car in the with id 'invalid_id'"
```
