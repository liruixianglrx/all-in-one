from eco_baseline.logic_tree.node import Node
from syn.tb_to_gate import gen_minterm, yosys_flow
from utils.min_term import MinTerms


class BaseNode:
    def __init__(
        self, node_list: list[Node], index_list: tuple[int], on_datas: list[list[int]]
    ) -> None:

        self.nodes = [node_list[index] for index in index_list]
        self.on_datas = list(set(map(tuple, on_datas)))

        self.minterms = MinTerms(list(map(list, set(map(tuple, on_datas)))))

    def gen_patch(self) -> None:
        variable_list = self.nodes_name

        # Only support 1 target node now.
        variable_list.append("t_0")

        # value_table = []
        # for truth_value in self.minterms.value:
        #     value_table.append(truth_value + [1])

        minterms = gen_minterm(variable_list, self.minterms.truth_table)
        yosys_flow(minterms, variable_list, silent=True)

    @property
    def nodes_name(self) -> list[str]:
        return [node.node_name for node in self.nodes]

    @property
    def rough_size(self) -> int:
        return self.minterms.rough_size

    @property
    def simple_str(self) -> str:
        return self.minterms.__repr__()

    def __str__(self) -> str:
        string = ""
        for node in self.nodes:
            string += "\n" + str(node)
        return "Basenode: " + string + self.minterms.__repr__()

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other) -> bool:
        return self.rough_size < other.rough_size
