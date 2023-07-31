from abc import abstractmethod

from eco_baseline.logic_tree.node import Node
from utils.utils import random_id


class Gate:
    def __init__(
        self, input_index: list[int], output_index: int, node_list: list[Node]
    ) -> None:
        """Base Gate constructor

        Args:
            input_index (list[int]): input nodes' indexes
            output_index (int): output node's index
            node_list (list[Node]): Circuit's node list
        """
        self.input_index = input_index
        self.output_index = output_index
        self.node_list = node_list

        self.id = random_id(2)

    @property
    def backward_done(self) -> bool:
        """Whether all the inputs have set level."""
        for i in self.input_index:
            if self.node_list[i].level_set_done is False:
                return False
        return True

    @abstractmethod
    def get_output_value(self) -> int:
        """Update the output node's value."""
        pass

    def set_output_value(self, value: int) -> None:
        assert value == 0 or 1, "Value invalid."
        self.node_list[self.output_index].set_value(value)
        # node_list 是node的lists

    def __str__(self) -> str:
        return (
            f"([{self.__class__.__name__}_{self.id}] "
            + f"inputs: {self.input_index}, output: {self.output_index})"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other) -> bool:
        self_out = self.node_list[self.output_index]
        other_out = self.node_list[other.output_index]

        return self_out.level < other_out.level


# ====== Gate Inheritances =====


class Not(Gate):
    def get_output_value(self) -> int:
        # input only has 1 node
        if self.node_list[self.input_index[0]].value == 1:
            self.set_output_value(0)
            return 0
        else:
            self.set_output_value(1)
            return 1


class Buf(Gate):
    def get_output_value(self) -> int:
        # only 1 input node
        input_value = self.node_list[self.input_index[0]].value
        self.set_output_value(input_value)
        return input_value


class And(Gate):
    def get_output_value(self) -> int:
        for i in self.input_index:
            # Has 0
            if self.node_list[i].value == 0:
                self.set_output_value(0)
                return 0
        else:
            # All 1
            self.set_output_value(1)
            return 1


class Nand(Gate):
    def get_output_value(self) -> int:
        for i in self.input_index:
            # Has 0
            if self.node_list[i].value == 0:
                self.set_output_value(1)
                return 1
        else:
            # All 1
            self.set_output_value(0)
            return 0


class Or(Gate):
    def get_output_value(self) -> int:
        for i in self.input_index:
            # Has 1
            if self.node_list[i].value == 1:
                self.set_output_value(1)
                return 1
        else:
            # All 0
            self.set_output_value(0)
            return 0


class Nor(Gate):
    def get_output_value(self) -> int:
        for i in self.input_index:
            # Has 1
            if self.node_list[i].value == 1:
                self.set_output_value(0)
                return 0
        else:
            # All 0
            self.set_output_value(1)
            return 1


class Xor(Gate):
    def get_output_value(self) -> int:
        # all instances of Xor only has 2 inputs
        value_0 = self.node_list[self.input_index[0]].value
        value_1 = self.node_list[self.input_index[1]].value

        if value_0 != value_1:
            self.set_output_value(1)
            return 1
        else:
            self.set_output_value(0)
            return 0


class Xnor(Gate):
    def get_output_value(self) -> int:
        # all instances of Xnor only has 2 inputs
        value_0 = self.node_list[self.input_index[0]].value
        value_1 = self.node_list[self.input_index[1]].value

        if value_0 == value_1:
            self.set_output_value(1)
            return 1
        else:
            self.set_output_value(0)
            return 0
