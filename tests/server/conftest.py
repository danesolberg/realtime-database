from queue import Queue
from pytest import fixture
from src.server.database_manager import DatabaseManager
from src.server.query_manager import SqlAlchemyQueryManager
from src.server.subscription_manager import SubscriptionManager
from src.server.subscription_tree import SubscriptionsRootNode
# from src.server import DatabaseManager, QueryManager, SubscriptionManager, SubscriptionsRootNode


@fixture
def db_manager():
    return DatabaseManager()

@fixture
def query_manager(db_manager):
    return SqlAlchemyQueryManager(db_manager)

@fixture
def subscription_manager(db_manager):
    return SubscriptionManager(db_manager, Queue)

@fixture
def subscription_tree():
    return SubscriptionsRootNode()
