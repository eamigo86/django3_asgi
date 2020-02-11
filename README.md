# django3_asgi

This is a test project of how to implement WebSockets with Django> = 3.0 without the need for any extra libraries:

_NOTE:_ Require Python 3.6 or higher

## How test it:

### Create a folder, clone the repo, create a virualenv and install the required packages:

```bash
mkdir django_websockets && cd django_websockets
python -m venv venv
source venv/bin/activate
git clone https://github.com/eamigo86/django3_asgi && cd django3_asgi
pip install -r requirements.txt
```

### Run Django migrations, create a superuser, and collect the static files (optional for admin only):

```bash
./manage.py migrate
./manage.py createsuperuser
./manage.py collectstatic
```

### Run the server, navigate to your admin enpoint and create some Car objects:

```bash
uvicorn --port 8000 websocket_app.asgi:application --reload
```
