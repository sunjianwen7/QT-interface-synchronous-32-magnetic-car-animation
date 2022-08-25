from peewee import Model,SmallIntegerField, SqliteDatabase, ForeignKeyField
#数据库路径
db = SqliteDatabase('AMGraph_Node/test.db')
# db = SqliteDatabase('test.db')
class Node_data(Model):
    node = SmallIntegerField(primary_key=True)
    rfid = SmallIntegerField()
    qt_x=SmallIntegerField()
    qt_y=SmallIntegerField()
    class Meta:
        database = db

class Edge_data(Model):
    node1 = ForeignKeyField(Node_data)
    node2 =  ForeignKeyField(Node_data)
    choose_= SmallIntegerField(Node_data)
    class Meta:
        database = db
def get_node_datas():
    node_datas = Node_data.select()
    return node_datas

def get_edge_datas():
    edge_datas = Edge_data.select()
    return edge_datas

def create_data():
    Node_data.create_table()
    Edge_data.create_table()
def get_node_rfid(rfid):
    result = Node_data.select().where(Node_data.rfid == rfid)
    if len(result)>0:
        return {'qt_x':result[0].qt_x,'qt_y':result[0].qt_y}
    else:
        return -1
def nodes_is_map(node1,node2):
    result1 = Node_data.select().where(Node_data.node == node1)
    result2 = Node_data.select().where(Node_data.node == node2)
    if len(result1)>0 and len(result2)>0:
        return True
    else:
        return False

if __name__ == '__main__':
    # pass
    create_data()
    # add_node_data()
    # a_l = get_node_datas()
    # for i in a_l:
    #     print(i)

