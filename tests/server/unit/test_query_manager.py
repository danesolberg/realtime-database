from ..testdata import QUERIES

def test_parse_string(db_manager, query_manager):
    for query_string, query_object in QUERIES:
        #TODO implement Query recursive equality code so these can be tested
        # directly rather than via __str__ representation
        assert str(query_manager.parse(db_manager.eval(query_string))) == str(query_object)