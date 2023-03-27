""" **************************************************************
* Programmer : Christopher K. Leung (2965-7518-69)               *
* Course ID  : CSCI531 - Applied Cryptography                    *
* Due Date   : March 26, 2023                                    *
* Project    : buildmtree.py                                     *
* Purpose    : This python script is to generate the merkle tree *
               for a set number of input CLI parameters          *
*****************************************************************"""

from treelib import Tree
import hashlib
import math
import sys


class treeNode:
    def __init__(self, data, left_node=None, right_node=None, uid=None):
        self.data = data
        self.hash = hashlib.sha256(data.encode()).hexdigest()
        self.left_node = left_node
        self.right_node = right_node
        self.uid = uid

    def node_print(self):
        print(f'UID:{self.uid}\r\nData:{self.data}\r\nHash:{self.hash}')

    def node_to_str(self):
        if self.left_node is None and self.right_node is None:
            return f'UID:{self.uid}\nData:{self.data}\nHash:{self.hash}\nL_Node:{self.left_node}\nR_Node:{self.right_node}\n\n'
        else:
            return f'UID:{self.uid}\nData:{self.data}\nHash:{self.hash}\nL_Node:{self.left_node.uid}\nR_Node:{self.right_node.uid}\n\n'

"""
Function :   get_remain_nodes
Parameters : list with names
Output :     remain:int
Description: determine number of nodes to make power of 2 at a certain level
"""
def get_remain_nodes(args):
    curr_level = math.log2(len(args))
    num_nodes = 0

    # Determine how many leaf nodes (2^L) where L is the level
    if math.ceil(curr_level) != math.floor(curr_level):
        num_nodes = math.pow(2, math.ceil(curr_level))

    # Remain variable used to determine how many leaf copies to make of the last node
    remain = int(num_nodes - len(args))

    return remain

"""
Function :   gen_tree
Parameters : CLI arguments
Output :     t:Tree
Description: Generate entire merkle tree bottom-up using treelib. Print to file shortly thereafter
"""
def gen_tree(args):
    t = Tree()
    remain = get_remain_nodes(args)
    leaves = []
    f = open("merkle.tree", "w")

    t.create_node(tag="Root", identifier="Root", parent=None, data=None)

    # copy all elements for CLI into leaf nodes
    for elem in range(len(args)):
        leaves.append(treeNode(args[elem]))

    # copy last element of leaf[len(args)] to satisfy power of 2
    for i in range(remain):
        leaves.append(treeNode(args[-1]))

    # add to tree
    for i in range(len(leaves)):
        uid = "d" + str(i)
        t.create_node(tag=None, identifier=uid, parent="Root", data=leaves[i].hash)
        leaves[i].uid = uid
        f.write(leaves[i].node_to_str())

    num_levels = int(math.floor(math.log2(len(leaves))))
    previous_level = leaves
    next_level = []
    hash_ctr = 0

    # Merkle Tree Bottom-Up Approach
    # 1. utilize num_levels to iteratively go through each tree's level performing bottom-up construction
    # 2. construct parent node by utilizing children indexed by left (2n) and right (2n+1) positions
    # 3. update L/R children to point at newly created parent
    # 4. store in local buffer (next_level) such that we have references to a previous level's nodes
    # 5. when num_levels reach 1, this is the root node. Store H(L+R) nodes
    for curr_level in range(num_levels, 0, -1):
        for i in range(0, len(previous_level), 2):
            l_node = previous_level[i]
            r_node = previous_level[i + 1]

            if curr_level != 1:
                node_id = "h" + str(hash_ctr)
            else:
                node_id = "Root"
            new_node = treeNode(l_node.hash + r_node.hash, l_node, r_node, node_id)
            f.write(new_node.node_to_str())

            if curr_level != 1:
                # print(f'[DEBUG]: L: {l_node} R: {r_node}')
                new_node.uid = node_id
                t.create_node(tag=None, identifier=node_id, parent="Root", data=new_node)
                t.move_node(l_node.uid, node_id)
                t.move_node(r_node.uid, node_id)
                next_level.append(new_node)
                hash_ctr += 1

            else:
                t.update_node("Root", data=new_node)

        previous_level = next_level.copy()
        next_level.clear()

    f.close()
    return t

"""
Function :   arg_parser
Parameters : CLI arguments
Output :     parsed_args:list[]
Description: Parse CLI to generate a list of names for data items in our merkle tree
"""
def arg_parser(args):
    temp_str = ""

    # iterate through args, concatenate into 1 string
    for x in range(1, len(args), 1):
        if args[x] == ',':
            continue
        temp_str += args[x]

    print(f'String: {temp_str}')

    # find brackets, returns -1 on failure
    l_bracket = temp_str.find('[')
    r_bracket = temp_str.find(']')

    # input sanitization
    if l_bracket >= 0 and r_bracket >= 0:
        temp_str = temp_str[l_bracket + 1:r_bracket:]
    elif l_bracket >= 0 > r_bracket:
        print(f'[ERROR]: Only Left bracket \'[\' found. Exiting now.')
        exit(-1)
    elif l_bracket < 0 <= r_bracket:
        print(f'[ERROR]: Only right bracket \']\' found. Exiting now.')
        exit(-1)

    parsed_args = temp_str.split(sep=',')

    if len(parsed_args) % 2 != 0:
        print(
            f'[WARN]: Input size is odd, appending last entry "{parsed_args[len(parsed_args) - 1]}" to make length even')
        parsed_args.append(parsed_args[len(parsed_args) - 1])

    return parsed_args

"""
Function :   merkle_entry
Parameters : CLI arguments
Output :     merkle tree
Description: Parse CLI to create merkle tree
"""
def merkle_entry(args):

    arguments = arg_parser(args)

    merkle_tree = gen_tree(arguments)

    merkle_tree.show()

    return merkle_tree


"""
Function :   main
Parameters : None
Output :     None
Description: Driver for build merkle tree
"""
if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print(f'[ERROR]: Not enough command line arguments\r\n'
              f'[Usage]: python buildmtree.py "[<data1,data2, ..., datan>]"\r\n'
              f'Exiting Now..')
        exit(-1)

    merkle_entry(args)
