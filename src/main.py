from server.wss import WebsocketsServer
from threading import Thread
import asyncio
from server.database_manager import DatabaseManager


if __name__ == "__main__":
    db = DatabaseManager()
    server = WebsocketsServer(db)

    db_monitor = Thread(target=server.sub_manager.process)
    event_monitor = Thread(target=server.push_changes)
    db_monitor.start()
    event_monitor.start()

    asyncio.run(server.main())