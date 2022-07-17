from collections import namedtuple
from queue import Queue
from typing import Dict, Iterable
from server.subscription_tree import SubscriptionsRootNode, TreeNode
from server.query_manager import SqlAlchemyQueryManager
from server.models import Query


Event = namedtuple("Event", ["subscriber_sockets", "table", "value"])

class SubscriptionManager:
    def __init__(self, db, event_queue):
        self.db = db
        self.query_ws_map = {}
        self.subscriber_tree = SubscriptionsRootNode()
        self.query_manager = SqlAlchemyQueryManager(db)
        self.db_change_queue = Queue()
        self.event_queue = event_queue

        self.db._set_queue(self.db_change_queue)

    def subscribe(self, ws, query_string: str):
        query_object = self.query_manager.parse(self.db.eval(query_string))
        # print("inserting query: " + query_string)
        query_id = self.db.insert(Query(content=query_string), False)
        query_object.id = query_id
        self.subscriber_tree.add_subscription(query_object)
        self.query_ws_map[query_id] = ws
        

    def unsubscribe(self, query_id):
        ...
        # if table in self.subscriber_tree:
        #     self.subscriber_tree[table].discard(ws)

    def query_to_websocket(self, queries: Iterable[int]):
        websockets= set()
        for query_id in queries:
            try:
                websockets.add(self.query_ws_map[query_id])
            except KeyError:
                raise ValueError("query_id missing from query to websocket mapping")
        return list(websockets)

    def find_subscribers(self, table:str, data: Dict):
        def dfs(node: TreeNode, path: str):
            # print(path)
            # print(node.subscribers)
            # print()
            if node.subscribers:
                subscribed_queries.update(node.subscribers)

            for col, val in data.items():
                if col in node.columns:
                    if val in node.columns[col]:
                        dfs(node.columns[col][val], path + " / " + str((col,val)))

        if table not in self.subscriber_tree.tables:
            return set()
        subscribed_queries = set()
        cur_node: TreeNode = self.subscriber_tree.tables[table]
        # print(f"searching for subs in table: {table} for data: {data}")
        dfs(cur_node, "")
        return self.query_to_websocket(subscribed_queries)

    def process(self):
        while True:
            db_change = self.db_change_queue.get()
            # print(db_change)
            row_id = db_change["_id"]
            table = db_change["table"]
            row_object = self.db.get(table, row_id).__dict__
            del row_object["_sa_instance_state"]

            subscriber_sockets = self.find_subscribers(table, row_object)
            self.event_queue.put(Event(subscriber_sockets, table, row_object))