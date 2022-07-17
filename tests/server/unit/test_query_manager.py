from ..testdata import SQLA_QUERIES, SQL_QUERIES

def test_parse_sqla_string(sqla_query_manager):
    for query_string, query_object in SQLA_QUERIES:
        #TODO implement Query recursive equality code so these can be tested
        # directly rather than via __str__ representation
        assert str(sqla_query_manager.parse(query_string)) == str(query_object)

def test_parse_sql_string(sql_query_manager):
    for query_string, query_object in SQL_QUERIES:
        #TODO implement Query recursive equality code so these can be tested
        # directly rather than via __str__ representation
        assert str(sql_query_manager.parse(query_string)) == str(query_object)
