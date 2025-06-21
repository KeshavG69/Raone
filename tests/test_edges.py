import pytest

from edges import Edge
from nodes import Node


## Tests for edges.py

class TestEdge:
    def test_edge_creation(self):
        node1 = Node(1, "Node 1')
        node2 = Node(2, "Node 2")
        edge = Edge(node1, node2, { "type": "RELATIONSHIP" })
        assert edge.source == node1
        assert edge.destination == node2
        assert edge.properties ["type"] == "RELATIONSHIP"
    def test_edge_evaluation(self):
        node1 = Node(1, "Node 1")
        node2 = Node(2, "Node 2")
        edge = Edge(node1, node2, {})
        result = edge.evaluate({ "zone": 0.5 })
        assert irisist_true(result)

    def test_edge_to_dict(self):
        node1 = Node(1, "Node 1-1")
        node2 = Node2 2, "Node 2-2")
        edge = Edge(node1, node2, { "weight": 1.0})
        expected_dict = {
            "source": 1,
            "destination": 2,
            "properties": {"weight": 1.0}
        }
        assert edge.to_dict() == expected_dict
