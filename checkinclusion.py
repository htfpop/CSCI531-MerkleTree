import hashlib
from treelib import Tree
import sys


class treeNode:
    def __init__(self, data, left_node=None, right_node=None, uid=None):
        self.data = data
        self.hash = hashlib.sha256(data.encode()).hexdigest()
        self.left_node = left_node
        self.right_node = right_node
        self.uid = uid

    def __str__(self):
        return f"Data: ({self.data}) Hash: ({hashlib.sha256(self.data.encode()).hexdigest()})"

    def node_print(self):
        print(f'UID:{self.uid}\r\nData:{self.data}\r\nHash:{self.hash}')

    def node_to_str(self):
        if self.left_node == 'None' and self.right_node == 'None':
            return f'UID:{self.uid}\nData:{self.data}\nHash:{self.hash}\nL_Node:{self.left_node}\nR_Node:{self.right_node}\n\n'
        else:
            return f'UID:{self.uid}\nData:{self.data}\nHash:{self.hash}\nL_Node:{self.left_node}\nR_Node:{self.right_node}\n\n'


def check_inclusion_entry():
    args = sys.argv
    if len(args) < 2:
        print(f'[ERROR]: No arguments provided. Exiting now')
        exit(-1)
    print(f'Arguments {args}\r\n')

    t = build_tree()
    #t.show()
    #list = t.paths_to_leaves()

    all_nodes = t.all_nodes()
    node_found: treeNode = None
    for node in all_nodes:
        if args[1] == node.data.data:
            node_found = node.data
            print(f'FOUND: {node_found.uid}')
            print(t.rsearch(node_found.uid))



def build_tree():
    t = Tree()
    t.create_node(tag="Root", identifier="Root")
    nodes = []
    curr_line = ""
    uid = None
    data = None
    hash = None
    l_node = None
    r_node = None

    with open('merkle.tree', 'r') as f:
        line_count = len(f.readlines())
        f.seek(0)

        for line in range(0, line_count, 6):
            uid = f.readline().split(':')[1].rstrip()
            data = f.readline().split(':')[1].rstrip()
            hash = f.readline().split(':')[1].rstrip()
            l_node = f.readline().split(':')[1].rstrip()
            r_node = f.readline().split(':')[1].rstrip()
            f.readline()
            new_node = treeNode(data=data, uid=uid)

            #nodes.append(treeNode(data, l_node, r_node, uid))
            if uid[0] == 'd':
                t.create_node(tag=None, identifier=uid, parent="Root", data=new_node)
            elif uid[0] == 'h':
                t.create_node(tag=None, identifier=uid, parent="Root", data=treeNode(data, t.get_node(l_node), t.get_node(r_node), uid))
                t.move_node(t.get_node(l_node).data.uid, uid)
                t.move_node(t.get_node(r_node).data.uid, uid)
            elif uid[0] == 'R':
                t.update_node("Root", data=treeNode(data, t.get_node(l_node), t.get_node(r_node), uid))

    for node in nodes:
        print(node.node_to_str())

    f.close()
    return t


if __name__ == '__main__':
    check_inclusion_entry()
