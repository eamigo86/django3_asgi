from asgiref.sync import sync_to_async


async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            break
        if event["type"] == "websocket.receive":
            await on_receive(event, receive, send)


async def on_receive(event, receive, send):
    if event["text"] == "car":
        from _test.models import Car

        car = await sync_to_async(Car.objects.first)()
        await send({"type": "websocket.send", "text": car.plate})

    elif event["text"] == "ping":
        await send({"type": "websocket.send", "text": "pong!"})

