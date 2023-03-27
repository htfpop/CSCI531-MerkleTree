""" **************************************************************
* Programmer : Christopher K. Leung (2965-7518-69)               *
* Course ID  : CSCI531 - Applied Cryptography                    *
* Due Date   : March 26, 2023                                    *
* Project    : checkconsistency.py                               *
* Purpose    : This python script is to determine if 2 merkle    *
               trees are similar                                 *
*****************************************************************"""

import hashlib
from treelib import Tree
import sys
import buildmtree
import checkinclusion


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
Function :   check_consistency_main
Parameters : None
Output :     None
Description: Generation of 2 trees to determine if they are consistent or not
"""
def check_consistency_main():
    args = sys.argv
    parent: treeNode = None
    node_found: treeNode = None
    l_node: treeNode = None
    r_node: treeNode = None
    proof = []
    is_power_2_arg1 = False
    is_power_2_arg2 = False

    if len(args) < 3:
        print(f'[ERROR]: Not enough command line arguments\r\n'
              f'[Usage]: python checkconsistency.py "[<Tree1>]" "[<Tree2>]"\r\n'
              f'Exiting Now..')
        exit(-1)

    f = open("merkle.trees", "w")
    f.write(f'--- Begin Tree 1 ---\n')

    # Create tree for first argument
    rep1, num_items1 = arg_parser(args[1])
    buildmtree.gen_tree(rep1)
    t: Tree = checkinclusion.build_tree()

    # read all contents from merkle.tree into merkle.trees
    f2 = open("merkle.tree", "r")
    f.write(f2.read())
    f.write(f'--- End Tree 1 ---\n')

    # separate Merkle Tree 1 from Merkle Tree 2
    f.write("\n")

    # Close merkle.tree, so it can be overwritten by second argument
    f2.close()

    # Create tree for second argument
    f.write(f'--- Begin Tree 2 ---\n')
    rep2, num_items2 = arg_parser(args[2])
    buildmtree.gen_tree(rep2)
    t2: Tree = checkinclusion.build_tree()
    f3 = open('merkle.tree', 'r')
    f.write(f3.read())
    f3.close()
    f.write(f'--- End Tree 2 ---\n')
    f.close()

    # iterate through every single item in rep1 and rep2 short circuit
    for item in range(0, num_items1, 1):
        if rep1[item] != rep2[item]:
            print('No')
            exit(-1)

    is_power_2_arg1 = is_power_of_two(num_items1)
    first_root: treeNode = t.get_node("Root").data

    if num_items1 % 2 == 1:
        proof.append(first_root.hash)
        mini_proof = checkinclusion.check_inclusion(t2, rep1[num_items1])
        proof.append(mini_proof)
        proof.append(t2.get_node("Root").data.hash)

    else:
        # obtain old root, next node and new root hash
        if is_power_2_arg1:
            proof.append(first_root.hash)
            proof.append(t2.get_node("Root").data.right_node.data.hash)
            proof.append(t2.get_node("Root").data.hash)

        # not power of 2 but even
        elif num_items1 % 2 == 0:
            child_uid = 'd' + str(num_items1 - 1)
            proof.append(first_root.hash)
            parent = t2.parent(child_uid)
            if child_uid == parent.data.left_node.data.uid:
                mini_proof = checkinclusion.check_inclusion(t2, parent.data.left_node.data.data)
                proof.append(mini_proof)
            else:
                mini_proof = checkinclusion.check_inclusion(t2, parent.data.right_node.data.data)
                proof.append(mini_proof)
            proof.append(t2.get_node("Root").data.hash)

    # proof output
    if len(proof) != 0:
        print(f'Yes, {proof}')
    else:
        print(f'No')


"""
    subset = None
    found = False
    for node in t2.all_nodes():
        instance = node.data
        if isinstance(instance, buildmtree.treeNode):
            if instance.hash == first_root.hash:
                subset = instance
                found = True
        elif isinstance(instance, str):
            if instance == first_root.hash:
                subset = node
                found = True

    if found:
        print(f'Found {first_root.hash} in new tree at index {subset.uid}')
    else:
        print(f'Not found')

    # t.show()
    # t2.show()
"""

"""
Function :   arg_parser
Parameters : program arguments
Output :     list and number of items before copy
Description: Argument parser that will take 2 input strings and create a tree
"""
def arg_parser(args):
    temp_str = args

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

    temp_str = temp_str.replace(" ", "")

    parsed_args = temp_str.split(sep=',')

    num_items = len(parsed_args)

    if len(parsed_args) % 2 != 0:
        #print(f'[WARN]: Input size is odd, appending last entry "{parsed_args[len(parsed_args) - 1]}" to make length even')
        parsed_args.append(parsed_args[len(parsed_args) - 1])

    #print(f'Args = {parsed_args}')

    return parsed_args, num_items

"""
Function :   is_power_of_two
Parameters : integer
Output :     True / False
Description: Determine if tree is a power of 2
"""
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0


"""
Function :   main
Parameters : None
Output :     None
Description: Check Consistency Driver
"""
if __name__ == '__main__':
    check_consistency_main()
