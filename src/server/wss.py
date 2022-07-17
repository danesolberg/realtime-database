import json
from queue import Queue
import websockets
import asyncio
from server.subscription_manager import SubscriptionManager
from server import logger


class WebsocketsServer:
    def __init__(self, db):
        self.db = db
        self.event_queue = Queue()
        self.sub_manager = SubscriptionManager(self.db, self.event_queue)
        
    def push_changes(self):
        while True:
            event = self.event_queue.get()
            payload = {
                "type": "mutation",
                "data": {
                    "table": event.table,
                    "value": event.value,
                }
            }
            # print("payload", payload)
            websockets.broadcast(event.subscriber_sockets, json.dumps(payload))


    async def mutate(self, event):
        action = event["action"]
        logger.info(f"Mutate event: {event}")
        # value = json.loads(event["value"])
        table = event["table"]
        value = event["value"]
        if action == "insert":
            self.db.insert(table, value)
        #TODO implement
        # elif action == "update":
        #     self.db.update(event["id"], value)
        # elif action == "replace":
        #     self.db.update(event["id"], value)

    async def subscribe(self, websocket, event):
        logger.info(f"Subscribed {websocket} to {event['query']}")
        
        self.sub_manager.subscribe(websocket, event["query"])
        await websocket.send(json.dumps({
            "type": "subscribed",
            "data": {
                "query": event["query"]
            }
        }))

    async def send_schema(self, websocket, event):
        if event.get("table"):
            schema = self.db.get_schema(event["table"])
            await websocket.send(json.dumps({
                "type": "schema",
                "data": {
                    "table": event["table"],
                    "schema": schema
                }
            }))

    async def handler(self, websocket):
        async for message in websocket:
            event = json.loads(message)

            if event["type"] == "subscribe":
                await self.subscribe(websocket, event["data"])
            elif event["type"] == "mutate":
                await self.mutate(event["data"])
            elif event["type"] == "get_schema":
                await self.send_schema(websocket, event["data"])

    async def main(self):
        async with websockets.serve(self.handler, "", 8001):
            await asyncio.Future()  # run forever
    