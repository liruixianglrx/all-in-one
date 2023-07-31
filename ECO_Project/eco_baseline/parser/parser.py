from eco_baseline.parser.grammar import verilog_grammar
from eco_baseline.parser.visitor import VerilogVisitor
from eco_baseline.logic_tree.node import Node


def str2node(str_list: list[str]) -> list[Node]:
    node_list = []
    for s in str_list:
        node_list.append(Node(s))

    return node_list


class VerilogParser:
    def __init__(self) -> None:
        self.grammar = verilog_grammar
        self.visitor = VerilogVisitor()

    def parse(self, content: str) -> dict:
        tree = self.grammar.parse(content)
        circuit_info = self.visitor.visit(tree)

        inst_list = ["NOT", "BUF", "AND", "NAND", "OR", "NOR", "XOR", "XNOR"]
        inst_dict = {}

        for inst in inst_list:
            if inst in circuit_info.keys():
                inst_dict[inst] = circuit_info.pop(inst)

        circuit_info["inst"] = inst_dict

        return circuit_info

    def read_file(self, file_path: str) -> dict:
        """Read verilog file and
            return a dictionary contains circuit information

        Args:
            file_path (str)

        Returns:
            dict: circuit information
        """
        with open(file_path, "r") as f:
            content = f.read()
        tree = self.grammar.parse(content)

        return self.parse(content)
