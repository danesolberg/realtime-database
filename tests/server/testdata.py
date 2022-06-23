from server import query_manager as qm

QUERIES = [
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
    qm.Query(
        "placeholder",
        "users",
        qm.ComplexPredicate(
            qm.PredicateType.OR,
            [
                qm.Boolean(
                    qm.BooleanOperator.GT,
                    "id",
                    5
                ),
                qm.ComplexPredicate(
                    qm.PredicateType.AND,
                    [
                        qm.Boolean(
                            qm.BooleanOperator.LT,
                            "id",
                            1000
                        ),
                        qm.ComplexPredicate(
                            qm.PredicateType.OR,
                            [
                                qm.Boolean(
                                    qm.BooleanOperator.EQ,
                                    "name",
                                    "Alice"
                                ),
                                qm.ComplexPredicate(
                                    qm.PredicateType.AND,
                                    [
                                        qm.Boolean(
                                            qm.BooleanOperator.GT,
                                            "age",
                                            10
                                        ),
                                        qm.Boolean(
                                            qm.BooleanOperator.EQ,
                                            "name",
                                            "Bob"
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                qm.ComplexPredicate(
                    qm.PredicateType.AND,
                    [
                        qm.Boolean(
                            qm.BooleanOperator.EQ,
                            "age",
                            50
                        ),
                        qm.Boolean(
                            qm.BooleanOperator.EQ,
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
        qm.Query(
            "placeholder",
            "users",
            qm.ComplexPredicate(
                qm.PredicateType.OR,
                [
                    qm.Boolean(
                        qm.BooleanOperator.GT,
                        "id",
                        5
                    ),
                    qm.ComplexPredicate(
                        qm.PredicateType.AND,
                        [
                            qm.Boolean(
                                qm.BooleanOperator.LT,
                                "id",
                                1000
                            ),
                            qm.ComplexPredicate(
                                qm.PredicateType.OR,
                                [
                                    qm.Boolean(
                                        qm.BooleanOperator.EQ,
                                        "name",
                                        "Alice"
                                    ),
                                    qm.ComplexPredicate(
                                        qm.PredicateType.AND,
                                        [
                                            qm.Boolean(
                                                qm.BooleanOperator.GT,
                                                "age",
                                                10
                                            ),
                                            qm.Boolean(
                                                qm.BooleanOperator.EQ,
                                                "name",
                                                "Bob"
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    qm.ComplexPredicate(
                        qm.PredicateType.AND,
                        [
                            qm.Boolean(
                                qm.BooleanOperator.EQ,
                                "age",
                                50
                            ),
                            qm.Boolean(
                                qm.BooleanOperator.EQ,
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