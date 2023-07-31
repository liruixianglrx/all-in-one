from copy import deepcopy

from eco_baseline.logic_tree import Gate, LogicTree, Node
from utils.utils import rm_duplicates

# TODO: Support multiple target nodes


class Pruner:
    def __init__(
        self, origin_logic_tree: LogicTree, golden_logic_tree: LogicTree
    ) -> None:
        """Structural Pruner

        Args:
            origin_logic_tree (LogicTree) \n
            golden_logic_tree (LogicTree)
        """
        self.origin = origin_logic_tree
        self.golden = golden_logic_tree

    def run_pruning(self, do_pruning=True):
        self.do_pruning = do_pruning

        if do_pruning:
            self._pruning()
            self._mask_logic_tree()

            print("Finish pruning.")
        else:
            self.origin.receive_mask(
                node_mask=[1] * self.origin.node_num,
                gate_mask=[1] * self.origin.gate_num,
            )
            self.golden.receive_mask(
                node_mask=[1] * self.golden.node_num,
                gate_mask=[1] * self.golden.gate_num,
            )

    def _pruning(self):
        """Main pruning process."""
        self.fanout_POs_og = []  # of origin
        self.fanin_PIs_gd = []  # of golden

        # Get the fanout_POs (of origin)
        for target_node in self.origin.target_nodes:
            self._find_fanout_PO(target_node)
        self.fanout_POs_og = rm_duplicates(self.fanout_POs_og)
        self.fanout_POs_og.sort()

        # Transfer origin fanout_POs to golden
        golden_PO = self.golden.output_nodes
        self.fanout_POs_gd = [
            golden_PO[golden_PO.index(po)] for po in self.fanout_POs_og
        ]

        # Get the fanin_PIs (of golden)
        for fanout_PO in self.fanout_POs_gd:
            self._find_fanin_PI(fanout_PO)
        self.fanin_PIs_gd = rm_duplicates(self.fanin_PIs_gd)
        self.fanin_PIs_gd.sort()

        # Transfer golden fanin_PIs to origin
        origin_PI = self.origin.input_nodes
        self.fanin_PIs_og = [origin_PI[origin_PI.index(pi)] for pi in self.fanin_PIs_gd]

        # Find all related fanouts with regard to fanin_PIs
        self.fanout_nodes_og_i, self.fanout_gates_og_i = self._find_all_fanout(
            logic_tree=self.origin, fanin_PIs=self.fanin_PIs_og
        )
        self.fanout_nodes_gd_i, self.fanout_gates_gd_i = self._find_all_fanout(
            logic_tree=self.golden, fanin_PIs=self.fanin_PIs_gd
        )

    def _find_fanout_PO(self, node: Node) -> None:
        """Find the fanout POs of the target node, in the origin logic tree."""
        if not node.load_index:
            self.fanout_POs_og.append(node)
        else:
            for load_gate_index in node.load_index:
                fanout_node_index = self.origin.gate_list[load_gate_index].output_index
                fanout_node = self.origin.node_list[fanout_node_index]
                self._find_fanout_PO(fanout_node)

    def _find_fanin_PI(self, node: Node) -> None:
        """Find the fanin PIs of the fanout_POs, in the golden logic tree."""
        if node in self.golden.input_nodes:
            self.fanin_PIs_gd.append(node)
        elif node.driver_index == -1:
            # Meet constant nodes
            return
        else:
            driver_gate = self.golden.gate_list[node.driver_index]
            for input_i in driver_gate.input_index:
                self._find_fanin_PI(self.golden.node_list[input_i])

    # TODO: Has a possible bug. Gate has only one input (BUF, NOT), will be added
    #   to the results.
    def _find_all_fanout(self, logic_tree: LogicTree, fanin_PIs: list[Node]):
        """Find all the fanouts of `fanin_PIs`, in both trees."""

        fanout_nodes_i = []
        fanout_gates_i = []

        fanout_nodes_i += [
            logic_tree.node_list.index(pi) for pi in fanin_PIs
        ]  # Append fanin_PIs first.
        fanout_nodes_i += logic_tree.target_nodes_i  # Append targets
        fanout_nodes_i += [
            logic_tree.node_num - 2,
            logic_tree.node_num - 1,
        ]  # Append constant

        node_list = logic_tree.node_list
        gate_list = deepcopy(logic_tree.gate_list)

        # Deal with t_* first
        for target_node_i in logic_tree.target_nodes_i:
            target_node = node_list[target_node_i]
            for load_gate_i in target_node.load_index:
                load_gate = gate_list[load_gate_i]

                if target_node_i in load_gate.input_index:
                    load_gate.input_index.remove(target_node_i)

        # Deal with constant (1'b0 / 1'b1)
        for i, const_node in enumerate(logic_tree.node_list[-2:]):
            node_i = logic_tree.node_num + i - 2
            for load_gate_i in const_node.load_index:
                load_gate = gate_list[load_gate_i]

                if node_i in load_gate.input_index:
                    load_gate.input_index.remove(node_i)

        # sub func
        def __sub_propagate(node: Node):

            node_i = node_list.index(node)

            # POs
            if not node.load_index:
                fanout_nodes_i.append(node_i)

            for load_gate_i in node.load_index:
                load_gate = gate_list[load_gate_i]

                if node_i in load_gate.input_index:
                    load_gate.input_index.remove(node_i)

                if not load_gate.input_index:
                    # If the input_index list is empty, go forward.
                    fanout_node_i = load_gate.output_index
                    fanout_node = node_list[fanout_node_i]
                    fanout_nodes_i.append(fanout_node_i)
                    fanout_gates_i.append(load_gate_i)
                    __sub_propagate(fanout_node)

        for pi in fanin_PIs:
            __sub_propagate(pi)

        fanout_nodes_i = rm_duplicates(fanout_nodes_i)
        fanout_gates_i = rm_duplicates(fanout_gates_i)
        return fanout_nodes_i, fanout_gates_i

    def _mask_logic_tree(self):
        def index_2_mask(indexes: list[int], node_num: int) -> list[int]:
            return [(1 if i in indexes else 0) for i in range(node_num)]

        self.origin.receive_mask(
            node_mask=index_2_mask(self.fanout_nodes_og_i, self.origin.node_num),
            gate_mask=index_2_mask(self.fanout_gates_og_i, self.origin.gate_num),
        )
        self.golden.receive_mask(
            node_mask=index_2_mask(self.fanout_nodes_gd_i, self.golden.node_num),
            gate_mask=index_2_mask(self.fanout_gates_gd_i, self.golden.gate_num),
        )

    def __repr__(self) -> str:
        repr = (
            f"Fanout POs: {self.fanout_POs_og}"
            + "\n"
            + f"Fanin PIs: {self.fanin_PIs_og}"
            + "\n"
            + f"All fanouts: {[self.origin.node_list[i] for i in self.fanout_nodes_og_i]}"
        )
        return repr

    @property
    def info(self):
        if self.do_pruning:
            print(f"Original node num: {self.origin.node_num}")
            print(f"After Pruning: {len(self.fanout_nodes_og_i)}")
            print(
                f"Pruning rate: {(1 - len(self.fanout_nodes_og_i) / self.origin.node_num):.3f}"
            )
