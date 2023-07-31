from itertools import compress

import numpy as np

import eco_baseline.logic_tree.gate as gate
import eco_baseline.eco_utils as eco_utils
from eco_baseline.logic_tree.node import Node


class LogicTree:
    def __init__(self, circuit_info: dict, verbose=False) -> None:
        self.circuit_info = circuit_info
        self.node_list = []
        self.gate_list = []
        self._read_circuit()

        if verbose:
            print("Nodes:", self.node_list)
            print("Gates:", self.gate_list)

    def _read_circuit(self) -> None:
        port_list = (
            self.circuit_info["input"]
            + self.circuit_info["output"]
            + self.circuit_info["wire"]
        )

        self.input_num = len(self.circuit_info["input"])
        self.output_num = len(self.circuit_info["output"])

        # Change the port name to Node
        for port in port_list:
            self.node_list.append(Node(port))

        # Add constant nodes
        constant_0 = Node("0")
        constant_1 = Node("1")
        constant_0.set_level(0)
        constant_1.set_level(0)
        constant_0.set_value(0)
        constant_1.set_value(1)

        self.node_list += [constant_0, constant_1]

        self.input_nodes = self.node_list[: self.input_num]
        self.output_nodes = self.node_list[
            self.input_num : self.input_num + self.output_num
        ]

        # This only works for ICCAD2017
        # Set the target node's level to 0
        self.target_num = 0
        self.target_nodes = []
        self.target_nodes_i = []
        for i, node in enumerate(self.node_list):
            if "t_" in node.node_name:
                node.set_level(0)
                self.target_nodes.append(node)
                self.target_nodes_i.append(i)
                self.target_num += 1

        # Instantiate all gates & update relations between Node and Gate.
        inst_list = []
        gate_index_count = 0  # help to locate

        # E.g. 'inst': {'AND': [['g1', 'a', 'b'], ['y1', 'g1', 'g2']]}
        inst_dict = self.circuit_info["inst"]
        for key, value in inst_dict.items():
            Inst = getattr(gate, key.capitalize())

            # Every port_list represents a gate.
            for port_list in value:
                # [0:1] means the first element, but as the only element in a list
                output_index = eco_utils.port_name_2_index(
                    port_list[0:1], self.node_list
                )[0]
                input_index = eco_utils.port_name_2_index(port_list[1:], self.node_list)
                gate_inst = Inst(input_index, output_index, self.node_list)
                self.gate_list.append(gate_inst)

                # Update node's load
                for input_i in input_index:
                    node = self.node_list[input_i]
                    node.add_load(gate_index_count)

                # Update node's driver
                node = self.node_list[output_index]
                node.set_driver(gate_index_count)

                # gate index++
                gate_index_count += 1

    def receive_mask(self, node_mask: list[int], gate_mask: list[int]) -> None:
        """Receive node mask and perform `node_backward`

        Args:
            node_mask (list[int])
            gate_mask (list[int])
        """
        self.node_mask = node_mask
        self.gate_mask = gate_mask

        self.masked_nodes = list(compress(self.node_list, self.node_mask))

        self.masked_input_nodes = list(
            compress(self.input_nodes, self.node_mask[: self.input_num])
        )

        self.masked_output_nodes = list(
            compress(
                self.output_nodes,
                self.node_mask[self.input_num : self.input_num + self.output_num],
            )
        )

        self.masked_node_num = len(self.masked_nodes)
        self.masked_input_num = len(self.masked_input_nodes)
        self.masked_output_num = len(self.masked_output_nodes)

        self._node_backward()

    def _node_backward(self) -> None:
        """Backward from output nodes, to determine the level of nodes."""

        # Set the primary input nodes' level to 0
        for primary_input in self.masked_input_nodes:
            primary_input.set_level(0)

        # Backward recursion
        for primary_out in self.masked_output_nodes:
            primary_out.get_level(self.node_list, self.gate_list)

        # Update target nodes' level according to their load
        for target_node in self.target_nodes:
            # target node is unlikely to have multiple load
            load_index = target_node.load_index[0]
            load_node_index = self.gate_list[load_index].output_index
            load_node_level = self.node_list[load_node_index].level
            new_target_level = load_node_level - 1
            target_node.level = new_target_level

        self.gate_forward_order = np.argsort(self.gate_list)[: sum(self.gate_mask)]

    def forward(self, input_data: list[int], target_data: list[int]):
        assert len(input_data) == self.masked_input_num, "Wrong input size"
        assert len(target_data) == self.target_num, "Wrong input size"

        # 将两个数组设值 masked_等都为node结构
        for i, input_node in enumerate(self.masked_input_nodes):
            input_node.set_value(input_data[i])

        # 将target节点值设置
        for i, target_node in enumerate(self.target_nodes):
            target_node.set_value(target_data[i])

        # 获得每个节点输出值
        for gate_index in self.gate_forward_order:
            self.gate_list[gate_index].get_output_value()

    def print_masked_circuit(self):
        print("Node:")
        for node in compress(self.node_list, self.node_mask):
            print(node)

        print("Gate:")
        for gate in compress(self.gate_list, self.gate_mask):
            print(gate)

    @property
    def node_num(self) -> int:
        return len(self.node_list)

    @property
    def gate_num(self) -> int:
        return len(self.gate_list)
