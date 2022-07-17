from enum import Enum
from typing import List, Union
from bisect import bisect_left
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList, Grouping
from collections import Iterable


class Condition:
    ...

class BooleanOperator(Enum):
    EQ = "eq"
    LT = "lt"
    GT = "gt"

class Boolean:
    def __init__(self, operator, column, value):
        self.op = operator
        self.column = column
        self.value = value

    def __str__(self):
        return f"Boolean {self.column} {self.op.value} {self.value}"

    def __repr__(self):
        return f"Boolean {self.column} {self.op.value} {self.value}"

class Query:
    def __init__(self, id, table, condition: Condition = None):
        self.id = id
        self.table = table
        self.condition = condition

    def __str__(self):
        return f"QUERY {self.id} on {self.table} -> {str(self.condition)}"

    def __repr__(self):
        return f"QUERY {self.id} on {self.table} -> {str(self.condition)}"

class PredicateType(Enum):
    AND = "and_"
    OR = "or_"
    
class ComplexPredicate(Condition):
    class BinarySearchKeyWrapper:
        def __init__(self, iterable, key):
            self.it = iterable
            self.key = key

        def __getitem__(self, i):
            return self.key(self.it[i])

        def __len__(self):
            return len(self.it)

    _bswrap = BinarySearchKeyWrapper

    def __init__(self, type: PredicateType, values: Union[Condition, List[Boolean]] = None):
        self.type = type

        # keep array of Boolean objects sorted by respective column name
        # to reduce size of subscription tree
        if isinstance(values, Iterable):
            self.values = []
            for condition in values:
                self.insert_condition(condition)
        elif isinstance(values, Condition):
            self.values = values
        elif values is None:
            self.values = []

    def insert_condition(self, cond):
        if isinstance(cond, Boolean):
            insert_idx = bisect_left(self._bswrap(self.values, key=lambda v: v.column if isinstance(v, Boolean) else "~"), cond.column)
            self.values.insert(insert_idx, cond)
        else:
            self.values.append(cond)

    def __str__(self):
        return f"Complex {self.type.value}({self.values})"

    def __repr__(self):
        return f"Complex {self.type.value}({self.values})"

class SimplePredicate(Condition):
    def __init__(self, bool: Boolean):
        self.bool = bool

    def __str__(self):
        return f"Simple {self.bool}"

    def __repr__(self):
        return f"Simple {self.bool}"


class SqlAlchemyQueryManager:
    def __init__(self, db):
        self.db = db

    def _process_clauses(self, query_id, table, clause):
        def inner(level, clause, context):
            if isinstance(clause, BinaryExpression):
                left, right, op = clause.left, clause.right, clause.operator
                # print(type(left), type(right), type(op))
                # print("_" * level, left.description)
                # print("_" * level, op.__name__)
                # print("_" * level, right.value)
                # print("_" * level, )

                bool = Boolean(
                            BooleanOperator(op.__name__),
                            left.description,
                            right.value
                        )

                if context is None:
                    query.condition = SimplePredicate(bool)
                else:
                    context.insert_condition(bool)
                    return context
                
            elif isinstance(clause, BooleanClauseList):
                op = clause.operator.__name__
                pred = ComplexPredicate(PredicateType(op))
                if context is None:
                    query.condition = pred
                    context = query.condition
                else:
                    context.insert_condition(pred)
                if PredicateType(op) == PredicateType.AND:
                    # print("_" * level, clause.operator.__name__)
                    for sub_clause in clause:
                        #TODO return relevant predicate object from inner()
                        # nest the conditions down the tree because its AND
                        pred = inner(level+1, sub_clause, pred)
                    return context
                elif PredicateType(op) == PredicateType.OR:
                    # print("_" * level, clause.operator.__name__)
                    for sub_clause in clause:
                        # keep all the conditions at the top level because its OR
                        inner(level+1, sub_clause, pred)
                    return context
                else:
                    raise ValueError("unknown PredicateType")
            elif isinstance(clause, Grouping):
                # print(dir(clause))
                # print(clause.expression)
                # print(type(clause.element))
                inner(level+1, clause.element, context)
            else:
                raise ValueError("unknown clause type")

        query = Query(query_id, table)
        inner(0, clause, None)
        return query

    def parse(self, sqla_query):
        clause = sqla_query.whereclause
        table = sqla_query.statement.froms[0].name
        # table = sqla_query.statement.get_final_froms()[0].name
        query_object = self._process_clauses("placeholder", table, clause)
        return query_object
