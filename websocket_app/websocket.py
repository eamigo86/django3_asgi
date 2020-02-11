import asyncio
import random

from asgiref.sync import sync_to_async


async def broadcast_messages(scope, send):
    client = ":".join(map(lambda x: str(x), scope["client"]))

    while True:
        timeout = random.randint(1, 6)
        await asyncio.sleep(timeout)

        await send(
            {
                "type": "websocket.send",
                "text": f"Server broadcast message to client '{client}', after {timeout} seconds",
            }
        )


async def websocket_application(scope, receive, send):
    loop = asyncio.get_event_loop()
    task = None

    while True:
        event = await receive()

        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})
            task = loop.create_task(broadcast_messages(scope, send))

        elif event["type"] == "websocket.disconnect":
            if task:
                task.cancel()
            break

        elif event["type"] == "websocket.receive":
            await on_receive(event, send)


async def on_receive(event, send):
    if "car" in event["text"].lower():
        from test_app.models import Car

        pk = event["text"].split(":")[1] if ":" in event["text"] else None

        if pk is not None or not str(pk).isnumeric():
            await send({"type": "websocket.send", "text": f"Invalid pk value: {pk}"})
        else:
            try:
                cars = await sync_to_async(Car.objects.all)()

                if pk:
                    car = await sync_to_async(cars.get)(id=int(pk))
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
