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


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

    args = sys.argv
    if len(args) < 2:
        print(f'[ERROR]: No arguments provided. Exiting now')
        exit(-1)
    print(f'Arguments {args}\r\n')
    arguments = arg_parser(args)

    merkle_tree = gen_tree(arguments)

    merkle_tree.show()


def gen_tree(args):
    t = Tree()
    level = math.log2(len(args))
    num_nodes = 0


    if math.ceil(level) != math.floor(level):
        num_nodes = math.pow(2, math.ceil(level))

    remain = int(num_nodes - len(args))

    t.create_node(tag="Root", identifier="Root", parent=None, data=None)

    leaf = []

    # copy all elements into leaf nodes
    for elem in range(len(args)):
        leaf.append(treeNode(args[elem]))

    for i in range(remain):
        leaf.append(treeNode(args[len(args) - 1]))

    for i in range(len(leaf)):
        print(leaf[i])

    print(f'test')
    #t.root = treeNode("test", leaf[int(len(args)/2)+2], leaf[int(len(args) / 2) + 1])

    print(f'Total nodes = {len(leaf)}')

    for i in range(len(leaf)-1, -1, -1):
        right = leaf[i]
        left = leaf[i-1]

        parent = t.create_node(right.data, right.data, t.root, hashlib.sha256((right.hash+left.hash).encode()).hexdigest())
        print(parent.data)

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
    elif l_bracket >= 0 and r_bracket < 0:
        print(f'[ERROR]: Only Left bracket \'[\' found. Exiting now.')
        exit(-1)
    elif l_bracket < 0 and r_bracket >= 0:
        print(f'[ERROR]: Only right bracket \']\' found. Exiting now.')
        exit(-1)

    print(f'String: {temp_str}')

    parsed_args = temp_str.split(sep=',')

    if len(parsed_args) % 2 != 0:
        print(f'[WARN]: Input size is odd, appending last entry "{parsed_args[len(parsed_args) - 1]}" to make length even')
        parsed_args.append(parsed_args[len(parsed_args) - 1])

    print(f'Args = {parsed_args}')

    return parsed_args


if __name__ == '__main__':
    print_hi('PyCharm')
