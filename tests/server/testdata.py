from server.query_managers import sqlalchemy as sa
from server.query_managers import pure_sql as ps

SQLA_QUERIES = [
    ("""session.query(User).where(
        or_(
            User.id>5, 
            and_(
                User.id<1000, 
                or_(
                    User.name=='Alice', 
                    and_(
                        User.name=='Bob', 
                        User.age>10
                    )
                )
            ), 
            and_(
                User.name=='Carol', 
                User.age==50
            )
        )
    )""",
    sa.Query(
        "placeholder",
        "users",
        sa.ComplexPredicate(
            sa.PredicateType.OR,
            [
                sa.Boolean(
                    sa.BooleanOperator.GT,
                    "id",
                    5
                ),
                sa.ComplexPredicate(
                    sa.PredicateType.AND,
                    [
                        sa.Boolean(
                            sa.BooleanOperator.LT,
                            "id",
                            1000
                        ),
                        sa.ComplexPredicate(
                            sa.PredicateType.OR,
                            [
                                sa.Boolean(
                                    sa.BooleanOperator.EQ,
                                    "name",
                                    "Alice"
                                ),
                                sa.ComplexPredicate(
                                    sa.PredicateType.AND,
                                    [
                                        sa.Boolean(
                                            sa.BooleanOperator.GT,
                                            "age",
                                            10
                                        ),
                                        sa.Boolean(
                                            sa.BooleanOperator.EQ,
                                            "name",
                                            "Bob"
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                sa.ComplexPredicate(
                    sa.PredicateType.AND,
                    [
                        sa.Boolean(
                            sa.BooleanOperator.EQ,
                            "age",
                            50
                        ),
                        sa.Boolean(
                            sa.BooleanOperator.EQ,
                            "name",
                            "Carol"
                        )
                    ]
                )
            ]
        )
    ))
]

SQL_QUERIES = [
    ("""
        SELECT *
        FROM users
        WHERE
            id > 5
            or (id < 1000 and (name = 'Alice' or (name = 'Bob' and age > 10)))
            or (name = 'Carol' and age = 50)
    """,
    ps.Query(
        "placeholder",
        "users",
        ps.ComplexPredicate(
            ps.PredicateType.OR,
            [
                ps.Boolean(
                    ps.BooleanOperator.GT,
                    "id",
                    5
                ),
                ps.ComplexPredicate(
                    ps.PredicateType.AND,
                    [
                        ps.Boolean(
                            ps.BooleanOperator.LT,
                            "id",
                            1000
                        ),
                        ps.ComplexPredicate(
                            ps.PredicateType.OR,
                            [
                                ps.Boolean(
                                    ps.BooleanOperator.EQ,
                                    "name",
                                    "Alice"
                                ),
                                ps.ComplexPredicate(
                                    ps.PredicateType.AND,
                                    [
                                        ps.Boolean(
                                            ps.BooleanOperator.GT,
                                            "age",
                                            10
                                        ),
                                        ps.Boolean(
                                            ps.BooleanOperator.EQ,
                                            "name",
                                            "Bob"
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                ps.ComplexPredicate(
                    ps.PredicateType.AND,
                    [
                        ps.Boolean(
                            ps.BooleanOperator.EQ,
                            "age",
                            50
                        ),
                        ps.Boolean(
                            ps.BooleanOperator.EQ,
                            "name",
                            "Carol"
                        )
                    ]
                )
            ]
        )
    ))
]

SUBSCRIPTIONS = [
    (
        """
        Root {
            'users': Treenode {
                'id': RangeDict{
                    RangeSet{Range(5, 1000)}: Treenode {
                        'name': RangeDict{
                            RangeSet{Range['Alice', 'Alice']}: Treenode {} subs:{'placeholder'}
                        }, 
                        'age': RangeDict{
                            RangeSet{Range(10, inf)}: Treenode {
                                'name': RangeDict{
                                    RangeSet{Range['Bob', 'Bob']}: Treenode {} subs:{'placeholder'}
                                }
                            } subs:set()
                        }
                    } subs:{'placeholder'}, 
                    RangeSet{Range[1000, inf)}: Treenode {} subs:{'placeholder'}, 
                    RangeSet{Range[-inf, 5]}: Treenode {
                        'name': RangeDict{
                            RangeSet{Range['Alice', 'Alice']}: Treenode {} subs:{'placeholder'}
                        }, 
                        'age': RangeDict{
                            RangeSet{Range(10, inf)}: Treenode {
                                'name': RangeDict{
                                    RangeSet{Range['Bob', 'Bob']}: Treenode {} subs:{'placeholder'}
                                }
                            } subs:set()
                        }
                    } subs:set()
                }, 
                'age': RangeDict{
                    RangeSet{Range[50, 50]}: Treenode {
                        'name': RangeDict{
                            RangeSet{Range['Carol', 'Carol']}: Treenode {} subs:{'placeholder'}
                        }
                    } subs:set()
                }
            } subs:set()
        }
        """,
        sa.Query(
            "placeholder",
            "users",
            sa.ComplexPredicate(
                sa.PredicateType.OR,
                [
                    sa.Boolean(
                        sa.BooleanOperator.GT,
                        "id",
                        5
                    ),
                    sa.ComplexPredicate(
                        sa.PredicateType.AND,
                        [
                            sa.Boolean(
                                sa.BooleanOperator.LT,
                                "id",
                                1000
                            ),
                            sa.ComplexPredicate(
                                sa.PredicateType.OR,
                                [
                                    sa.Boolean(
                                        sa.BooleanOperator.EQ,
                                        "name",
                                        "Alice"
                                    ),
                                    sa.ComplexPredicate(
                                        sa.PredicateType.AND,
                                        [
                                            sa.Boolean(
                                                sa.BooleanOperator.GT,
                                                "age",
                                                10
                                            ),
                                            sa.Boolean(
                                                sa.BooleanOperator.EQ,
                                                "name",
                                                "Bob"
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    sa.ComplexPredicate(
                        sa.PredicateType.AND,
                        [
                            sa.Boolean(
                                sa.BooleanOperator.EQ,
                                "age",
                                50
                            ),
                            sa.Boolean(
                                sa.BooleanOperator.EQ,
                                "name",
                                "Carol"
                            )
                        ]
                    )
                ]
            )
        )
    )
]