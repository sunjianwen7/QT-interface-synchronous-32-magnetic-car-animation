import networkx as nx
import AMGraph_Node
from AMGraph_Node.model import get_node_rfid


class Map():
    def create_graph(self):
        self.map = nx.DiGraph()
    def add_edge(self,node1,node2,choose_):
        self.map.add_edges_from([
            (node1,node2,{'choose':choose_})
        ])

    def add_node(self,node,rfid,qt_x,qt_y):
        self.map.add_node(node,rfid=rfid,pose=(qt_x,qt_y))

    def ShortestPath(self,srart_node,end_node):
        nodes = nx.shortest_path(self.map,srart_node,end_node)
        node_edge = []
        for i in range(len(nodes)-1):
            node_edge.append(self.map.get_edge_data(nodes[i],nodes[i+1]))
        return node_edge,nodes

