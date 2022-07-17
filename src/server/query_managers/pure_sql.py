from enum import Enum, EnumMeta
from mo_sql_parsing import parse
from server.query_managers.base import Boolean, SimplePredicate, ComplexPredicate, Query


class MyEnumMeta(EnumMeta):  
    def __contains__(cls, item): 
        return item in cls.__members__.values()

class BooleanOperator(str, Enum, metaclass=MyEnumMeta):
    EQ = "eq"
    LT = "lt"
    GT = "gt"

class PredicateType(str, Enum, metaclass=MyEnumMeta):
    AND = "and"
    OR = "or"

class PureSqlQueryManager:
    @classmethod
    def parse(cls, sql_query):
        parsed_results = parse(sql_query)

        if "where" not in parsed_results:
            # primary key range (-inf, inf)
            ...
        else:
            clause = parsed_results["where"]
            table = parsed_results["from"]
            query_object = cls._process_clauses("placeholder", table, clause)
        return query_object

    @staticmethod
    def _process_clauses(query_id, table, clause):
        def inner(level, clause, context):
            # print(level, clause)
            key = next(iter(clause))
            if key in BooleanOperator:
                op = key
                left = clause[key][0]
                right = clause[key][1]
                if isinstance(right, dict):
                    right = right[next(iter(right))]

                bool = Boolean(
                            BooleanOperator(op),
                            left,
                            right
                        )

                if context is None:
                    query.condition = SimplePredicate(bool)
                else:
                    context.insert_condition(bool)
                    return context
                
            elif key in PredicateType:
                op = key
                pred = ComplexPredicate(PredicateType(op))
                if context is None:
                    query.condition = pred
                    context = query.condition
                else:
                    context.insert_condition(pred)
                if PredicateType(op) == PredicateType.AND:
                    # print("_" * level, clause.operator.__name__)
                    for sub_clause in clause[key]:
                        #TODO return relevant predicate object from inner()
                        # nest the conditions down the tree because its AND
                        pred = inner(level+1, sub_clause, pred)
                    return context
                elif PredicateType(op) == PredicateType.OR:
                    # print("_" * level, clause.operator.__name__)
                    for sub_clause in clause[key]:
                        # keep all the conditions at the top level because its OR
                        inner(level+1, sub_clause, pred)
                    return context
                else:
                    raise ValueError("unknown PredicateType")
            else:
                raise ValueError("unknown clause type")

        query = Query(query_id, table)
        inner(0, clause, None)
        return query
