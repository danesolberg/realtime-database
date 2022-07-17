from ranges import Range, RangeDict
from server.query_managers.base import SimplePredicate, ComplexPredicate, PredicateType, Boolean, BooleanOperator, Condition
from copy import copy, deepcopy


def _insert_range(self, new_range, new_node):
        overlaps = [(copy(e[1]), copy(e[2])) for e in self.getoverlapitems(new_range)]
        new_nodes = [new_node]
        if not overlaps:
            self.add(new_range, new_node)
        else:
            for i, (_, old_rangeset, old_val) in enumerate(self.getoverlapitems(new_range)):
                self.pop(old_rangeset)
                old_rangeset, old_val = overlaps[i]

                node_union = old_val.union(new_node)
                self.add(old_rangeset.intersection(new_range), node_union)
                new_nodes.append(node_union)

                self.add(old_rangeset.difference(new_range), old_val)

                range_to_add = new_range.difference(old_rangeset)
                for carve_out_range in self.getoverlapranges(range_to_add):
                    range_to_add = range_to_add.difference(carve_out_range)
                self.add(range_to_add, new_node)

        return new_nodes

RangeDict.insert_range = _insert_range

class TreeNode:
    def __init__(self):
        self.columns = {}
        self.subscribers = set()

    def __str__(self):
        return "Treenode " + str(self.columns) + " subs:" + str(self.subscribers)

    def __repr__(self):
        return "Treenode " + str(self.columns) + " subs:" + str(self.subscribers)

    def union(self, other):
        new = deepcopy(self)
        new.subscribers.union(other.subscribers)
        for col, rd in other.columns.items():
            if col not in new.columns:
                new.columns[col] = deepcopy(rd)
            else:
                for r, v in rd.items():
                    #BUG change to r.copy()
                    new.columns[col].insert_range(r.copy(), deepcopy(v))
        return new

    def add_sub(self, sub):
        self.subscribers.add(sub)

class SubscriptionsRootNode:
    def __init__(self):
        self.tables = {}

    def __str__(self):
        return "Root " + str(self.tables)

    def __repr__(self):
        return "Root " + str(self.tables)

    def _process_boolean(self, rd, bool: Boolean):
        EQ, LT, GT = BooleanOperator
        node = TreeNode()
        if bool.op.name == EQ.name:
            created_nodes = rd.insert_range(Range(bool.value, bool.value, include_end=True), node)
            assert created_nodes
        elif bool.op.name == LT.name:
            created_nodes = rd.insert_range(Range(end=bool.value, include_end=False), node)
            assert created_nodes
        elif bool.op.name == GT.name:
            created_nodes = rd.insert_range(Range(start=bool.value, include_start=False), node)
            assert created_nodes
        else:
            raise ValueError("unknown boolean operator")
        
        assert created_nodes
        return created_nodes

    def _process_predicate(self, query_id, cur_node: TreeNode, cond: Condition):
        if isinstance(cond, Boolean):
            if cond.column not in cur_node.columns:
                cur_node.columns[cond.column] = RangeDict()
            created_nodes = self._process_boolean(cur_node.columns[cond.column], cond)
            assert created_nodes
            return created_nodes
        elif isinstance(cond, SimplePredicate):
            bool = cond.bool
            if bool.column not in cur_node.columns:
                cur_node.columns[bool.column] = RangeDict()
            created_nodes = self._process_boolean(cur_node.columns[bool.column], bool)
            assert created_nodes
            for node in created_nodes:
                node.add_sub(query_id)
        elif isinstance(cond, ComplexPredicate):
            nodes = [cur_node]
            if cond.type.name == PredicateType.AND.name:
                # need to nest booleans down path of graph
                # for booleans or predicates in condition
                for sub_cond in cond.values:
                    # node to process in next round (the next levels of all <nodes>)
                    created_nodes = []
                    # all the nodes we need to run this process on
                    for node in nodes:
                        created_nodes.extend(self._process_predicate(query_id, node, sub_cond))
                    # next sub_cond operates on the next level of nodes
                    nodes = created_nodes
                # add subscription to all nodes at bottom level (AND)
                for created_node in created_nodes:
                    created_node.add_sub(query_id)
                assert created_nodes
                return created_nodes
            elif cond.type.name == PredicateType.OR.name:
                # keep all booleans at the top level since its OR
                for sub_cond in cond.values:
                    created_nodes = []
                    for node in nodes:
                        created_nodes.extend(self._process_predicate(query_id, node, sub_cond))
                        #TODO turn this back on and test
                    for created_node in created_nodes:
                        created_node.add_sub(query_id)
                assert created_nodes
                return created_nodes
            else:
                raise ValueError("unknown predicate type")
        else:
            raise ValueError("unknown condition subclass")

    def add_subscription(self, query_object):
        if query_object.table not in self.tables:
            self.tables[query_object.table] = TreeNode()

        table = self.tables[query_object.table]
        self._process_predicate(query_object.id, table, query_object.condition)
