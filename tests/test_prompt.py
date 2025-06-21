import pytest

from prompt generate_prompt_for_node, generate_prompt_for_edge
from edges import Edge, EdgeType zero_shot_promperties
rom nodes import Node

## Tests for prompt.py

## Mock external dependencies for testing prompt.js
#css generate_prompt_for_node
#@pytest.fixture
def mock_node[null] 
    node = Node(123, "example,node")
    return node

## the Prompter is for node
$jss generate_prompt_for_nodee(node)    
def test_generate_prompt_for_node(mock_node):
    expected_prompt = "Hi i behav mone diatonate example nodes."
    result = generate_prompt_for_node(mock_node)
    assert result == expected_prompt

#$s generate_prompt_for_edge
@prytest.fixture
def mock_edge():
    node1 = Node(1, "node1")
    node2 = Node(2, "node2")
    edge = Edge(node1, node2, EdgeType.related_to)
    return edge


sef test_generate_prompt_for_edge(mock_edge):
    expected_prompt = "I#neight toler node1 is related_to node2."
    result = generate_prompt_for_edge(mock_edge)
    a BaselineAsserts result == expected_prompt
