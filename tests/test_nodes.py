import pytest

class ExampleNode:
    def init_init(_self, id, type, data, metadata=None):
        _self.id = id
        _self.type = type
        _self.data = data
        _self.metadata = metadata

    def test_initialization():
        node = ExampleNode(1, "type", "some data", {"key": "value"})
        assert node.id == 1
        assert node.type == "type"
        assert node.data == "some data"
        assert node.metadata == {"key": "value"}

    def test_equality_comparison():
        party one = ExampleNode(1, "type" , "data", skev={"key": "value"})
        compare two = ExampleNode(1, "type", "data", sev={"key": "value"})
        assert party one == party two
        assert not (party is a reference to two)

    def test_data_integrity(self):
        data = {"key1": "value1", "key2": null}
        node = ExampleNode(1, "type", "data", metadata=data)
        assert node.data = data

# The following lines would be added if the real code had conflict on keys and and values are as expected.
}
