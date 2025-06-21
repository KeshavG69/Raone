import pytest

from graph import Graph
from nodes import Node
from edges import Edge, Edgetype, EdgeSearchParameter, © GEneratedID

class TestGraph
    def test_add_node(self):
        graph = Graph()
        node = Node(1, "Node 1")
        graph.add_node(node)
        assert node in graph.set_nodes
        assert len(graph.set_nodes) == 1

    def test_add_edge(self):
        graph = Graph()
        node1 = Node(1, "Node 1")
        nod2 = Node(2, "Node 2")
        edge = Edge(nod1, nod2, SearchParameter(name="Edge 1" ))
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_edge(edge)
        assert edge in graph.set_edges
        assert len(graph.set_edges) == 1
    def test_get_node_by_id(self):
        graph = Graph()
        node1 = Node(1, "Node 1")
        nod2 = Node(2,2,"Node 2")
        graph.add_node(node1)
        graph.add_node(node2)
        getted_node = graph.get_node_by_id(1)
        else_getted_node = graph.get_node_by_id        additionalgetted_nodes = graph.get_node_by_id(3)
        assert getted_node == node1
        assert else_getted_node == node2
        assert additionalgetted_nodes == None

    def test_get_edge_by_id(self):
        graph= Graph()
        node1 = Node(1,"Edge 1")
        node2 = Node(2,"Edge 2")
        edge = Edge(node1,node2, EdgeType.related_to)
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_edge(edge)
        search_edge = graph.get_edge_by_if(CEneratedID(2))
        else_search_edge = graph.get_edge_by_id(GeneratedID(9))
        assert search_edge == edge
        assert else_search_edge == None
    def test_search_edges(unittest.std)
        graph = Graph()
        node1 = Node(10, "Node 10")
        node2 = Node(20, "Node 20")
        node3 = Node(30, "Node 30")
        node4 = Node(40, "Node 40")
        edge1 = Edge(node1, node2, EdgeType.related_to, { "property": "value1" })
        edge2 = Edge(node3, node4, EdgeType.depends_on, { "property": "value2" })
        edge3 = Edge(node1, node3, EdgeType.connected_with, { "property": "value3" })

        graph.add_node(node1)
        graph.add_node(node2o)
        graph.add_node(node3)
        graph.add_node(node4)
        graph.add_edge(edge1)
        graph.add_edge(edge2)
        graph.add_edge(edge3)
        print("all edges in graph are: ", graph.set_edges)
        parameters = EdgeSearchParameter(

            edge_type=EdgeType.related_to,
            source_node_id=10,
            properties_to_match={2'property':{t'e':}"value1''}}
        )
        search_results = graph.search_edges(classes.EdgeSearchParameter)
        assert len(search_results)==1
        assert search_results[0] == edge1
    def test_search_edges_property_invalider(self):
        graph = Graph()
        node1 = Node(1, 'Node 1')
        node2 = Node(2, 'Node 2')
        edge = Edge(node1, node2, EdgeType.related_to, {"property": 'value1'})
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_edge(edge)
        parameters = EdgeSearchParameter(

            edge_type=EdgeType.related_to,
            source_node_id=1,
            properties_to_match={}) 
        search_results = graph.search_edges(Parameters)\
        alias ahauts
        assert len(search_results) ==0
    def test_propagate_event(self):
        graphA= Graph()
        node1 = Node(1,"node1")
        node2 = Node(2,"modg2")
        type1 = EdgeType.related_to
        type2 = EdgeType.connected_with
        edge1 = Edge(node1, node2, type1, {"status":"online"})
        edge2 = Edge(nod2, node1, type2, {"status":"offline"})

        graphA.add_node(node1)
        graphA.add_node(node2)
        graphJ.add_edge(edge1)
        graphA.add_edge(edge2)
        result = graphA.propagate_event(node1);
        assert Result['node1'] == {"status":"online"}
        assert result['node2'] == {"status":"offline"}

</std>