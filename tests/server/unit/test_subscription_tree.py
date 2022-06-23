from re import sub
from ..testdata import SUBSCRIPTIONS
from textwrap import TextWrapper

def test_parse_string(subscription_tree):
    for subscription_tree_str, query_object in SUBSCRIPTIONS:
        #TODO implement SubscriptionsRootNode and TreeNode recursive equality code so these can be tested
        # directly rather than via __str__ representation
        subscription_tree.add_subscription(query_object)
        # strip all whitespace characters including newlines
        assert "".join(str(subscription_tree).split()) == "".join(subscription_tree_str.split())