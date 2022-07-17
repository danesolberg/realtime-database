from queue import Queue
from pytest import fixture
from src.server.database_manager import DatabaseManager
from server.query_managers.sqlalchemy import SqlAlchemyQueryManager
from server.query_managers.pure_sql import PureSqlQueryManager
from src.server.subscription_manager import SubscriptionManager
from src.server.subscription_tree import SubscriptionsRootNode


@fixture
def db_manager():
    return DatabaseManager()

@fixture
def sqla_query_manager(db_manager):
    return SqlAlchemyQueryManager(db_manager)

@fixture
def sql_query_manager():
    return PureSqlQueryManager()

@fixture
def subscription_manager(db_manager):
    return SubscriptionManager(db_manager, Queue)

@fixture
def subscription_tree():
    return SubscriptionsRootNode()
