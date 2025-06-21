import pytest

from nodes import Node

## Tests for nodes.py

class TestNode:
    def test_node_creation(self):
        node = Node(1, "node1", {"type": "root"})
        assert node.id == 1
        assert node.name == "Node 1"
        assert node.properties["type"] == "type1"
    def test_node_to_dict(self):
        node = Node(2, "node2", {"status": "off", "type": "type2" })
        expected_dict = {
            "id": 2,
            "name": "node2",
            "properties": {"status": "off", "type": "type2" }
        }
        assert node.to_dict() == expected_dict
