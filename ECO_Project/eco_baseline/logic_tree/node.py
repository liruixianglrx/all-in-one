# from eco_baseline.logic_tree.gate import Gate
INIT_LEVEL = 9999


class Node:
    def __init__(self, node_name: str) -> None:
        self.node_name = node_name
        # Set level to INIT_LEVEL
        self.level = INIT_LEVEL
        # Set value -1 => not decided yet
        self.value = -1
        self.driver_index = -1
        # 有哪些相关门与该节点关联
        self.load_index = []

    def set_driver(self, gate_index: int):
        """Set the driver to Node"""
        assert self.driver_index == -1, "Node's driver has already set."
        self.driver_index = gate_index

    def add_load(self, load_index: int):
        """Add a load to Node"""
        self.load_index.append(load_index)

    def set_level(self, level: int) -> None:
        assert not self.level_set_done, "Node's level has already set."
        self.level = level

    def get_level(self, node_list, gate_list) -> int:
        if self.level_set_done:
            return self.level
        else:
            driver_gate = gate_list[self.driver_index]
            input_node_level = []
            for driver_gate_input in driver_gate.input_index:
                input_node = node_list[driver_gate_input]
                input_node_level.append(input_node.get_level(node_list, gate_list))

            self.set_level(max(input_node_level) + 1)
            return self.level

    def set_value(self, value: int) -> None:
        self.value = value

    def clear_value(self) -> None:
        self.value = -1

    @property
    def level_set_done(self) -> bool:
        """Return whether the node's level has been set."""
        return self.level != INIT_LEVEL

    def __str__(self) -> str:
        return f"([{self.node_name}][Lv:{self.level}], Value:{self.value}, DRV:{self.driver_index}, LD:{self.load_index})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.node_name == other.node_name

    def __hash__(self) -> int:
        return hash(self.node_name)

    def __lt__(self, other) -> bool:
        return self.node_name < other.node_name
