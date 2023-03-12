import hashlib
from treelib import Node, Tree
import os
import sys


# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

    args = sys.argv
    print(f'Arguments {args}\r\n')
    arg_parser(args)

    t = Tree()
    t.create_node("Harry", "harry")
    t.create_node("Jane", "jane", parent="harry")
    t.create_node("Bill", "bill", parent="harry")
    t.create_node("Diane", "diane", parent="jane")
    t.create_node("Mary", "mary", parent="diane")
    t.create_node("Mark", "mark", parent="jane")

    t.show()


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

    print(f'Args = {parsed_args}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
