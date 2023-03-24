from treelib import Node, Tree
import hashlib
import math
import sys


class treeNode:
    def __init__(self, data, left_node=None, right_node=None):
        self.data = data
        self.hash = hashlib.sha256(data.encode()).hexdigest()
        self.left_node = left_node
        self.right_node = right_node

    def __str__(self):
        return f"Data: ({self.data}) Hash: ({hashlib.sha256(self.data.encode()).hexdigest()})"


def merkle_entry():
    args = sys.argv
    if len(args) < 2:
        print(f'[ERROR]: No arguments provided. Exiting now')
        exit(-1)
    print(f'Arguments {args}\r\n')
    arguments = arg_parser(args)

    merkle_tree = gen_tree(arguments)

    merkle_tree.show()


def get_remain_nodes(args):
    curr_level = math.log2(len(args))
    num_nodes = 0

    # Determine how many leaf nodes (2^L) where L is the level
    if math.ceil(curr_level) != math.floor(curr_level):
        num_nodes = math.pow(2, math.ceil(curr_level))

    # Remain variable used to determine how many leaf copies to make of the last node
    remain = int(num_nodes - len(args))

    return remain


def gen_tree(args):
    t = Tree()
    remain = get_remain_nodes(args)
    leaves = []

    t.create_node(tag="Root", identifier="Root", parent=None, data=None)

    # copy all elements for CLI into leaf nodes
    for elem in range(len(args)):
        leaves.append(treeNode(args[elem]))

    # copy last element of leaf[len(args)] to satisfy power of 2
    for i in range(remain):
        leaves.append(treeNode(args[-1]))

    # DEBUG
    for i in range(len(leaves)):
        print(f'[DEBUG]: {leaves[i]}')

    print(f'Total nodes = {len(leaves)}')

    #    for i in range(len(leaf) - 1, -1, -1):
    #        right = leaf[i]
    #        left = leaf[i - 1]

    #        parent = t.create_node(right.data, right.data, t.root,
    #                               hashlib.sha256((right.hash + left.hash).encode()).hexdigest())
    #        print(parent.data)

    for i in range(0, len(leaves), 2):
        l_node = leaves[i]
        r_node = leaves[i + 1]

        print(f'[DEBUG]: L: {l_node} R: {r_node}')

    return t


def arg_parser(args):
    parsed_args = []
    l_bracket = -99
    r_bracket = -99
    temp_str = ""

    # iterate through args, concatenate into 1 string
    for x in range(1, len(args), 1):
        if args[x] == ',':
            print(f'continued from white space')
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

    print(f'String: {temp_str}')

    parsed_args = temp_str.split(sep=',')

    if len(parsed_args) % 2 != 0:
        print(
            f'[WARN]: Input size is odd, appending last entry "{parsed_args[len(parsed_args) - 1]}" to make length even')
        parsed_args.append(parsed_args[len(parsed_args) - 1])

    print(f'Args = {parsed_args}')

    return parsed_args


if __name__ == '__main__':
    merkle_entry()
