from queue import Queue
from typing import Dict
from uuid import UUID, uuid4
from sqlalchemy import create_engine, and_, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from server.models import Base, User, Query
from server import logger


# class Value:
#     def __init__(self, value: Dict):
#         self.object = value

# class Document:
#     def __init__(self, table: str, value: Dict):
#         self.id = uuid4()
#         self.table = table
#         self.value = Value(value)
#         self.value.object["_id"] = str(self.id)

#     def _update(self, value: Value):
#         for k, v in value.object.items():
#             if k == "_id":
#                 continue
#             self.value.object[k] = v

#     def _replace(self, value: Value):
#         self.value = value
#         self.value.object["_id"] = self.id

# class Table:
#     def __init__(self, name):
#         self.name = name
#         self.documents = []

#     def __hash__(self):
#         return hash(self.name)

#     def _insert(self, value):
#         document_object = Document(self.name, value)
#         self.documents.append(document_object)
#         return document_object

class DatabaseManager:
    def __init__(self):
        self.tables = {}
        self.documents = {}
        self.change_queue = None
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False}, 
            poolclass=StaticPool,
            echo=False
        )

        Base.metadata.create_all(self.engine)

    def _publish(self, document_id: int, table: str):
        if self.change_queue:
            self.change_queue.put({
                "_id": document_id,
                "table": table
            })

    def _set_queue(self, queue: Queue):
        self.change_queue = queue

    def insert(self, value: str, deserialize=False):
        # if table not in self.tables:
        #     self.tables[table] = Table(table)
        # table_object = self.tables[table]
        # document_object = table_object._insert(value)
        # id = document_object.id
        # self.documents[id] = document_object

        if deserialize:
            row = self.eval(value)
        else:
            row = value
        logger.info(f"INSERT: {row}")
        with Session(self.engine) as session, session.begin():
            session.add(row)
            session.flush()
            # print(row)
            id = row.id
            table = row.__tablename__
            session.commit()

        self._publish(id, table)

        return id

    def get(self, table_name, id):
        table = Base.TBLNAME_TO_CLASS[table_name]
        with Session(self.engine) as session, session.begin():
            row = session.scalars(select(table).where(getattr(table, "id")==id)).first()
            session.expunge(row)
            logger.info(f"GET: {row} from table {table}")
            return row

    def update(self, id, value):
        # if id in self.documents:
        #     document_object = self.documents[id]
        #     document_object._update(value)
        #     self._publish(document_object.id)
        ...

    def replace(self, id, value):
        # if id in self.documents:
        #     document_object = self.documents[id]
        #     document_object._replace(value)
        #     self._publish(document_object.id)
        ...

    def eval(self, value):
        with Session(self.engine) as session, session.begin():
            return eval(value)