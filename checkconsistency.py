import hashlib
from treelib import Tree
import sys
import buildmtree


class treeNode:
    def __init__(self, data, left_node=None, right_node=None, uid=None):
        self.data = data
        self.hash = hashlib.sha256(data.encode()).hexdigest()
        self.left_node = left_node
        self.right_node = right_node
        self.uid = uid

        # def __str__(self):
        # return self.uid
        # return f"Data: ({self.data}) Hash: ({hashlib.sha256(self.data.encode()).hexdigest()})"

    def node_print(self):
        print(f'UID:{self.uid}\r\nData:{self.data}\r\nHash:{self.hash}')

    def node_to_str(self):
        if self.left_node is None and self.right_node is None:
            return f'UID:{self.uid}\nData:{self.data}\nHash:{self.hash}\nL_Node:{self.left_node}\nR_Node:{self.right_node}\n\n'
        else:
            return f'UID:{self.uid}\nData:{self.data}\nHash:{self.hash}\nL_Node:{self.left_node.uid}\nR_Node:{self.right_node.uid}\n\n'


def check_consistency_main():
    args = sys.argv
    parent: treeNode = None
    node_found: treeNode = None
    l_node: treeNode = None
    r_node: treeNode = None
    proof = []
    success = False

    if len(args) < 3:
        print(f'[ERROR]: Not enough arguments provided. Exiting now')
        exit(-1)
    print(f'Arguments {args}\r\n')

    rep1 = arg_parser(args[1])
    rep2 = arg_parser(args[2])

    t: Tree = buildmtree.gen_tree(rep1)
    t2: Tree = buildmtree.gen_tree(rep2)

    t.show()
    t2.show()


def arg_parser(args):
    temp_str = args

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
    temp_str = temp_str.replace(" ", "")

    parsed_args = temp_str.split(sep=',')

    if len(parsed_args) % 2 != 0:
        print(
            f'[WARN]: Input size is odd, appending last entry "{parsed_args[len(parsed_args) - 1]}" to make length even')
        parsed_args.append(parsed_args[len(parsed_args) - 1])

    print(f'Args = {parsed_args}')

    return parsed_args


if __name__ == '__main__':
    check_consistency_main()
