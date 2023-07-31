import numpy as np
import pandas as pd

from syn.tb_to_gate import gen_minterm, yosys_flow
from eco_baseline.parser import VerilogParser


class MinTerms:
    def __init__(self, value: list[list[int]]) -> None:
        self.value = value

        self.node_num = len(self.value[0])
        self.min_term_num = len(self.value)
        self.truth_table = [term + [1] for term in self.value]

    def get_gate_num(self, tmp_path="tmp") -> int:
        """Get the corresponding circuit's gate number."""

        self._synthesis(tmp_path)

        vp = VerilogParser()
        circuit_info = vp.read_file(f"./{tmp_path}/synth.v")
        gate_num = 0
        for gate, inst in circuit_info["inst"].items():
            gate_num += len(inst)

        return gate_num

    def get_distance_tuple(self) -> tuple[int]:
        """Get the sum of distances of minterms.

        Returns:
            int: the distance
        """
        if self.min_term_num == 1:
            return (0,)

        distance_matrix = (
            np.ones((self.min_term_num, self.min_term_num)) * self.node_num
        )

        distance_sum = []

        for index_1 in range(self.min_term_num):
            for index_2 in range(index_1 + 1, self.min_term_num):
                dist = self._distance(index_1, index_2)
                distance_matrix[index_1][index_2] = dist
                distance_matrix[index_2][index_1] = dist

            distance_sum.append(np.min(distance_matrix[index_1]))

        return tuple(distance_sum)

    def _distance(self, index_1: int, index_2: int) -> int:
        """Get the distance between 2 minterms."""
        assert index_1 < self.min_term_num
        assert index_2 < self.min_term_num

        d = 0
        for i in range(self.node_num):
            d += abs(self.value[index_1][i] - self.value[index_2][i])
        return d

    def _synthesis(self, tmp_path):
        fake_variable_list = ["g" + str(i) for i in range(self.node_num)] + ["t"]

        yosys_flow(
            gen_minterm(fake_variable_list, self.truth_table),
            fake_variable_list,
            tmp_path=tmp_path,
            silent=True,
        )

    def model_predict_size(self, estimator) -> float:
        cols = ["node_num", "minterm_num", "distance"]
        if self.min_term_num == 1 or self.min_term_num == 2**self.node_num - 1:
            return self.node_num - 1

        distance = sum(self.get_distance_tuple())

        data = pd.DataFrame(
            [[self.node_num, self.min_term_num, distance]],
            columns=cols,
        )
        predict_size = estimator.predict(data).item()
        return predict_size

    @property
    def rough_size(self) -> int:
        return self.node_num * self.min_term_num

    def __repr__(self) -> str:
        return f"(Node_num: {self.node_num}, minterm_num: {self.min_term_num})"
