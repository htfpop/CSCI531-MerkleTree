""" **************************************************************
* Programmer : Christopher K. Leung (2965-7518-69)               *
* Course ID  : CSCI531 - Applied Cryptography                    *
* Due Date   : March 26, 2023                                    *
* Project    : checkinclusion.py                                 *
* Purpose    : This python script is to determine if a name from *
               is included within our merkle tree                *
*****************************************************************"""

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

    def node_to_str(self):
        if self.left_node == 'None' and self.right_node == 'None':
            return f'UID:{self.uid}\nData:{self.data}\nHash:{self.hash}\nL_Node:{self.left_node}\nR_Node:{self.right_node}\n\n'
        else:
            return f'UID:{self.uid}\nData:{self.data}\nHash:{self.hash}\nL_Node:{self.left_node}\nR_Node:{self.right_node}\n\n'

"""
Function :   check_inclusion_entry
Parameters : CLI Arguments
Output :     None
Description: Prints "Yes" with merkle proof to indicate inclusion or "no" if person is not in the tree
"""
def check_inclusion_entry():
    args = sys.argv

    if len(args) < 2:
        print(f'[ERROR]: Not enough command line arguments\r\n'
              f'[Usage]: python checkinclusion.py "<person>"\r\n'
              f'Exiting Now..')
        exit(-1)
    print(f'Arguments {args}\r\n')

    t = build_tree()
    proof = check_inclusion(t, args[1])

    if len(proof) == 0:
        print('No')
    else:
        print(f'Yes, {proof}')

"""
Function :   check_inclusion
Parameters : t:tree, search_val:str
Output :     proof:list[]
Description: Prepends proof of inclusion for merkle tree
"""
def check_inclusion(t, search_val):
    parent: treeNode = None
    node_found: treeNode = None
    l_node: treeNode = None
    r_node: treeNode = None
    proof = []
    success = False

    all_nodes = t.all_nodes()

    for node in all_nodes:
        if search_val == node.data.data:
            node_found = node.data
            success = True
            print(f'FOUND: {node_found.uid}')
            break

    if success:
        while node_found.uid != 'Root':
            parent = t.parent(node_found.uid)
            l_node = parent.data.left_node.data
            r_node = parent.data.right_node.data

            if l_node.uid == node_found.uid:
                proof.append(r_node.hash)
            else:
                proof.append(l_node.hash)

            node_found = parent.data

    return proof

"""
Function :   build_tree
Parameters : CLI Arguments
Output :     t:Tree
Description: Parses merkle.tree and re-creates the tree data structure accordingly 
"""
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

        # python line parser
        for line in range(0, line_count, 6):
            uid = f.readline().split(':')[1].rstrip()
            data = f.readline().split(':')[1].rstrip()
            hash = f.readline().split(':')[1].rstrip()
            l_node = f.readline().split(':')[1].rstrip()
            r_node = f.readline().split(':')[1].rstrip()
            f.readline()
            new_node = treeNode(data=data, uid=uid)

            # 'd' == data item, 'h' = hash(d<n> || d<n>) , 'r' == Root
            if uid[0] == 'd':
                t.create_node(tag=None, identifier=uid, parent="Root", data=new_node)
            elif uid[0] == 'h':
                t.create_node(tag=None, identifier=uid, parent="Root",
                              data=treeNode(data, t.get_node(l_node), t.get_node(r_node), uid))
                t.move_node(t.get_node(l_node).data.uid, uid)
                t.move_node(t.get_node(r_node).data.uid, uid)
            elif uid[0] == 'R':
                t.update_node("Root", data=treeNode(data, t.get_node(l_node), t.get_node(r_node), uid))

    for node in nodes:
        print(node.node_to_str())

    f.close()
    return t

"""
Function :   main
Parameters : None
Output :     None
Description: Driver for check inclusion
"""
if __name__ == '__main__':
    check_inclusion_entry()
