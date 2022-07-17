from enum import Enum
from typing import List, Union
from bisect import bisect_left
from collections import Iterable


BooleanOperator = Enum('BooleanOperator', 'EQ LT GT')

PredicateType = Enum('PredicateType', 'AND OR')

class Condition:
    ...

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

    def __init__(self, type: Enum, values: Union[Condition, List[Boolean]] = None):
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
