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
    if "car" in event["text"].lower():
        from test_app.models import Car

        pk = int(event["text"].split(":")[1]) if ":" in event["text"] else None

        try:
            cars = await sync_to_async(Car.objects.all)()

            if pk:
                car = await sync_to_async(cars.get)(id=pk)
            else:
                car = await sync_to_async(cars.first)()
            await send({"type": "websocket.send", "text": car.plate})
        except Car.DoesNotExist:
            await send(
                {
                    "type": "websocket.send",
                    "text": f"Do not exists any car in the with id '{pk}'",
                }
            )

    elif event["text"] == "ping":
        await send({"type": "websocket.send", "text": "pong!"})

