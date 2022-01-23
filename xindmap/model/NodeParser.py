import re

from .Data import Data
from .Node import Node
from .NodeParsingError import NodeParsingError

class NodeParser:
    """Parses and writes files containing node tree.
    """
    def __init__(self):
        self.__data_pattern = '.*'
        self.__node_pattern = 'Node \d \({}\)'.format(self.__data_pattern)
        self.__line_pattern = ' *{}'.format(self.__node_pattern)

    def parse_node(self, node_string):
        """Parses a string to create a node with no parent.

        Parses string following the expected pattern:

            Node id (data)

        where:
            * id is an integer used to identify the node
            * data is a string that can be parsed by method `parse_data`

        Args:
            node_string: the string to parse.

        Returns:
            A node with no parent.

        Raises:
            NodeParsingError: when a parsing error occurs while parsing the string.
        """
        if not re.fullmatch(self.__node_pattern, node_string):
            raise NodeParsingError('"{}" does not match expected pattern for a node'.format(node_string))

        node_string_split = node_string.split()
        node_id = int(node_string_split[1])
        node_data_string = node_string_split[2][1:-1]
        node_data = self.parse_data(node_data_string)

        return Node(node_id, None, node_data)

    def parse_data(self, data_string):
        """Parses a string to create a data.

        Parses string following the expected pattern:

            text

        where:
            * text is the text contained in the data

        Args:
            data_string: the string to parse.

        Returns:
            A data.

        Raises:
            NodeParsingError: when a parsing error occurs while parsing the string.
        """
        if not re.fullmatch(self.__data_pattern, data_string):
            raise NodeParsingError('"{}" does not match expected pattern for a data'.format(data_string))

        return Data(data_string)

    def parse_file(self, file_path):
        """Parses a file to create a tree of nodes.

        Parses a file following the expected pattern:

            [index_block]node

        where:
            * node is a string that can be parsed by `parse_node`
            * [indent_block] is a block composed of any number of spaces, can
              be repeated any number of times. The number of spaces must be
              consistent accross the file.

        With this pattern, an entire tree can be expressed.
        The first node in the file should not be not be indented and is the root
        of the tree. 
        Every other nodes need to be indented so that its parent can be
        identified.
        Therefore, every nodes indented under a node is considered to be among
        its children.

        Args:
            file_path: the path to the file to parse.

        Returns:
            The root node of the tree.

        Raises:
            NodeParsingError: when a parsing error occurs while parsing the file.
        """
        root_node = None
        line_index = 0
        indent_expected_size = None
        previous_node = None
        previous_node_level = None

        with open(file_path, 'r') as file:
            for line in file:
                # remove last char that must be the carriage return
                line = line[:-1]

                if not re.fullmatch(self.__line_pattern, line):
                    raise NodeParsingError('error at line {}: "{}" does not match expected pattern'.format(line_index, line))

                # retrieve info from line
                indent_block = line[0:line.index('N')]
                indent_block_size = len(indent_block)
                node_string = line[line.index('N'):]
                node = self.parse_node(node_string)

                # root node
                if root_node is None:
                    if indent_block_size > 0:
                        raise NodeParsingError('error at line {}: expected root node to not be indented'.format(line_index))

                    root_node = node
                    node_level = 0
                # other nodes
                else:
                    if indent_expected_size is None:
                        indent_expected_size = indent_block_size

                    if indent_block_size % indent_expected_size != 0:
                        raise NodeParsingError('error at line {}: unexpected indent'.format(line_index))

                    node_level = indent_block_size // indent_expected_size

                    if node_level == previous_node_level:
                        node.parent = previous_node.parent
                        previous_node.parent.children.append(node)

                    elif node_level == previous_node_level + 1:
                        node.parent = previous_node
                        previous_node.children.append(node)

                    elif node_level < previous_node_level:
                        node.parent = previous_node.parent
                        for _ in range(previous_node_level - node_level):
                            node.parent = node.parent.parent
                        node.parent.children.append(node)

                    else:
                        raise NodeParsingError('error at line {}: incoherent node level'.format(line_index))

    
                line_index += 1
                previous_node = node
                previous_node_level = node_level

        return root_node

    def write_to_file(self, root_node, file_path):
        """Writes a node tree to a file that can be parsed by self.

        Args:
            root_node: the root of the tree
            file_path: the path to the file in which write the tree
        """
        def recursive_write_to_file(node, node_level):
            file.write('{}{}\n'.format('    ' * node_level, node))

            for child in node.children:
                recursive_write_to_file(child, node_level + 1)

        with open(file_path, 'w') as file:
            recursive_write_to_file(root_node, 0)

