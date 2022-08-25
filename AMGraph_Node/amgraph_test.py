from AMGraph_Node.AMGraph import Map
from AMGraph_Node.model import get_node_datas, get_edge_datas
class AMD_Map():
    def __init__(self):
        map = Map()
        map.create_graph()
        node_datas = get_node_datas()
        for i in node_datas:
            map.add_node(i.node, i.rfid, i.qt_x, i.qt_y)
        for i in get_edge_datas():
            map.add_edge(i.node1.node, i.node2.node, i.choose_)
        self.map=map
    def test(self):
        node_edge, nodes = self.map.ShortestPath(3, 5)
        for i in zip(nodes, node_edge):
            print(i)
    def Calculate_path(self,node1,node2):
        node_edge, nodes = self.map.ShortestPath(node1,node2)
        return zip(nodes, node_edge),nodes[-1]
if __name__ == '__main__':
    amd=AMD_Map()
    amd.Calculate_path(3,5)
