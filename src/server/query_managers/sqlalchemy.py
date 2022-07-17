from enum import Enum
from sqlalchemy.sql.elements import BinaryExpression, BooleanClauseList, Grouping
from server.query_managers.base import Boolean, SimplePredicate, ComplexPredicate, Query


class BooleanOperator(Enum):
    EQ = "eq"
    LT = "lt"
    GT = "gt"

class PredicateType(Enum):
    AND = "and_"
    OR = "or_"

class SqlAlchemyQueryManager:
    def __init__(self, db):
        self.db = db
        
    @staticmethod
    def _process_clauses(query_id, table, clause):
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
        sqla_query = self.db.eval(sqla_query)
        clause = sqla_query.whereclause
        table = sqla_query.statement.froms[0].name
        # table = sqla_query.statement.get_final_froms()[0].name
        query_object = self._process_clauses("placeholder", table, clause)
        return query_object
