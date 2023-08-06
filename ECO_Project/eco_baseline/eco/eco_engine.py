import math
import hypergbm
from itertools import combinations
import json
import eco_baseline.eco.MyEncoder as my_encoder
from random import sample
import eco_ext
import numpy as np
import time

import eco_baseline.eco_utils as eco_utils
from eco_baseline.eco.base_node import BaseNode
from eco_baseline.eco.pruner import Pruner
from eco_baseline.eco.verification import Miter
from eco_baseline.logic_tree import LogicTree
from eco_baseline.parser import VerilogParser
from syn.tb_to_gate import gen_minterm, yosys_flow
from utils.utils import *
from multiprocessing import Pool, Manager

MAX_TRAVERSE_NUM = 10


class EcoEngine:
    def __init__(
        self,
        original_file_path: str,
        golden_file_path: str,
        early_stop=10,
        do_pruning=True,
    ) -> None:
        self.original_file_path = original_file_path
        self.golden_file_path = golden_file_path

        parser = VerilogParser()
        self.origin = LogicTree(parser.read_file(original_file_path), verbose=False)
        self.golden = LogicTree(parser.read_file(golden_file_path), verbose=False)
        assert self.origin.input_num == self.golden.input_num, "Logic tree unmatch."
        # self.input_num = self.origin_logic_tree.input_num

        self.miter = Miter(
            original_file_path,
            golden_file_path,
            input_num=self.origin.input_num,
            output_num=self.origin.output_num,
        )

        pruner = Pruner(self.origin, self.golden)
        pruner.run_pruning(do_pruning)
        print(pruner.info)
        # print(self.origin.masked_nodes)

        self.masked_input_num = (
            self.origin.masked_input_num
        )  # Both tree has the same input num

        # If input num is too large, using sampling.
        if self.masked_input_num > MAX_TRAVERSE_NUM:
            print("ECO Sampling Enable")
            self.sampling = True
        else:
            print("ECO Traverse.")
            self.sampling = False

        # All PIs and nodes other than POs, target and constants.
        self.possible_candidate_node_index = list(range(self.masked_input_num)) + list(
            range(
                self.masked_input_num + self.origin.masked_output_num,
                len(self.origin.masked_nodes) - 3,
            )
        )

        print("Target level: ", self.origin.target_nodes[0].level)

        self.candidate_basenodes = []
        self.candidate_early_stop = early_stop

        self.estimator = read_pickle("./size_predictor/model.pkl")

    def run_eco(
        self,
        searching_node_range: list[int],
        stratified=True,
        levels_per_layer=2,
        comb_max=3000,
        max_try=10,
        max_subtry=3,
        max_subsubtry=15,
        print_mean_size=True,
        minimizing=True,
    ):
        """Main Process

        Args:
            searching_node_range (list[int])
            stratified (bool, optional): Defaults to True.
            levels_per_layer (int, optional): Defaults to 2.
            max_try (int, optional): Defaults to 50.
        """
        self.iter = 0

        self.comb_max = comb_max
        self.searching_node_range = searching_node_range
        self.minimizing = minimizing

        find_func = self._find_candidate_base

        if stratified and self._stratify(levels_per_layer):
            find_func = self._priority_find_candidate_base

            # To identify whether a layer has been fully searched
            self.fully_searched = []

        if self.sampling:
            for try_i in range(max_try):
                print(f"Try: {try_i+1}")
                print("Node range: ", self.searching_node_range)
                # print(f"Searching candidate with ")

                passed_list = []
                self.candidate_basenodes = []

                sub_try = 0
                while not self.reach_early_stop and sub_try < max_subtry:
                    sub_try += 1
                    print("Sub try:", sub_try)

                    self._run_traverse()
                    if not self.on_index:
                        print("No on-set")
                        continue

                    subsub_try = 0
                    while not self.reach_early_stop and subsub_try < max_subsubtry:
                        subsub_try += 1
                        print("Subsub try:", subsub_try)
                        find_func(self.searching_node_range, levels_per_layer)
                        if self.reach_early_stop:
                            break

                    if self.reach_early_stop:
                        break

                for candidate in sorted(self.candidate_basenodes):
                    verify_state = self.miter.verify(candidate)
                    if verify_state:
                        passed_list.append(candidate)
                    # if len(passed_list) >= self.candidate_early_stop:
                    #     break

                if passed_list:
                    if print_mean_size:
                        print(
                            "Mean: ",
                            np.mean([b.minterms.get_gate_num() for b in passed_list]),
                        )
                    print("Found passed candidate")
                    if self.minimizing:
                        best_candidate, min_size = self._model_predict_best(passed_list)
                    else:
                        best_candidate = random.choice(passed_list)
                    # self.generate_patch(best_candidate)
                    print(best_candidate)
                    print("ECO Success !!")
                    print("Patch size: ", best_candidate.minterms.get_gate_num())
                    return
                else:
                    print("ECO Failed")
                    self.searching_node_range = [
                        n + 1 for n in self.searching_node_range
                    ]

        # Not sampling
        else:
            self.candidate_basenodes = []
            self._run_traverse()
            while not self.reach_early_stop:
                find_func(self.searching_node_range, levels_per_layer)

            if print_mean_size:
                print(
                    "Mean: ",
                    np.mean(
                        [b.minterms.get_gate_num() for b in self.candidate_basenodes]
                    ),
                )

            if self.minimizing:
                predict_list = sorted(self.candidate_basenodes)[:5]

                best_candidate, min_size = self._model_predict_best(predict_list)

                print("Smallest size: ", min_size)
            else:
                best_candidate = random.choice(self.candidate_basenodes)

            self.generate_patch(best_candidate)
            print("Patch: ", best_candidate)

            if self.miter.verify(best_candidate):
                print("ECO Success !!")
                print("Patch size: ", best_candidate.minterms.get_gate_num())
                return

    def _model_predict_best(self, candidate_list: list[BaseNode]):
        min = 1e10
        best_candidate = candidate_list[0]
        for candidate in candidate_list:
            # predict_size = candidate.minterms.model_predict_size(self.estimator)
            predict_size = candidate.minterms.get_gate_num()
            if predict_size < min:
                best_candidate = candidate
                min = predict_size

        return best_candidate, min

    def _run_traverse(self):
        if self.sampling:
            # 得到随机的input
            inputs = random_input_vec(
                input_num=self.masked_input_num, n=2**MAX_TRAVERSE_NUM
            )
        else:
            #得到_input_signals的样式的input
            inputs = self._input_signals(node_num=self.masked_input_num)

        self._write_logic_tree(self.origin,self.masked_input_num,"origin_logic_tree.txt")
        self._write_logic_tree(self.golden, self.masked_input_num,"golden_logic_tree.txt")

        start_time = time.time()
        self._traverse_golden(inputs)
        self._traverse_origin(inputs)
        end_time = time.time()
        run_time = end_time - start_time
        print("程序运行时间：", run_time * 1e6, "us")

        self._find_on_off()
        # print("ON:", self.on_index)
        # print("OFF:", self.off_index)

    def _write_logic_tree(self, tree : LogicTree, masked_input_num :int,name : str):
        name ="/home/lrx/Desktop/all-in-one/txts/"+name;
        file = open(name, "w")
        tstr = "*node_list :\n"
        file.write(tstr)
        for i, node in enumerate(tree.node_list):
            json_str = json.dumps(node, cls=my_encoder.MyEncoder)
            file.write(json_str)
            file.write("\n")

        tstr = "*masked_input_nodes :\n"
        file.write(tstr)
        for i, node in enumerate(tree.masked_input_nodes):
            json_str =json.dumps(node,cls=my_encoder.MyEncoder)
            file.write(json_str)
            file.write("\n")

        tstr = "*target_nodes :\n"
        file.write(tstr)
        for i, node in enumerate(tree.target_nodes):
            json_str =json.dumps(node,cls=my_encoder.MyEncoder)
            file.write(json_str)
            file.write("\n")

        tstr = "*gate_forward_order :\n"
        file.write(tstr)
        json_str = json.dumps(tree.gate_forward_order.tolist())
        file.write(json_str)
        file.write("\n")

        tstr = "*gate_list :\n"
        file.write(tstr)
        for i, gate in enumerate(tree.gate_list):
            json_str = json.dumps(gate, cls=my_encoder.MyEncoder)
            file.write(json_str)
            file.write("\n")

        tstr = "*masked_output_nodes :\n"
        file.write(tstr)
        for i, node in enumerate(tree.masked_output_nodes):
            json_str = json.dumps(node, cls=my_encoder.MyEncoder)
            file.write(json_str)
            file.write("\n")

        tstr = "*masked_input_num: \n"
        file.write(tstr)
        file.write(str(masked_input_num))
        file.write("\n")

        tstr = "*target_num: \n"
        file.write(tstr)
        file.write(str(tree.target_num))
        file.write("\n")

        tstr = "*masked_nodes :\n"
        file.write(tstr)
        for i, node in enumerate(tree.masked_nodes):
            json_str = json.dumps(node, cls=my_encoder.MyEncoder)
            file.write(json_str)
            file.write("\n")

        file.close()


    def _traverse_golden(self, golden_inputs: np.ndarray):
        self.golden_output_results = np.ndarray(
            (golden_inputs.shape[0], self.golden.masked_output_num), dtype=np.int8
        )

        for i, golden_input in enumerate(golden_inputs):
            # golden logic tree
            self.golden.forward(golden_input, [])
            result = eco_utils.nodes_2_values(self.golden.masked_output_nodes)
            self.golden_output_results[i] = result

    def _traverse_origin(self, origin_inputs: np.ndarray):
        """Only support 1 target now."""
        self.origin_results = np.ndarray(
            (2, origin_inputs.shape[0], self.origin.masked_node_num), dtype=np.int8
        )

        target_inputs = [[0], [1]]

        for target_input in target_inputs:
            results_of_one_target = []
            for i, origin_input in enumerate(origin_inputs):
                self.origin.forward(origin_input, target_input)
                result = eco_utils.nodes_2_values(self.origin.masked_nodes)

                # target_input[0] -> change list to a value
                self.origin_results[target_input[0], i] = result

    def _find_on_off(self):
        """Find on-set and off-set"""
        self.on_index = []
        self.off_index = []

        if self.sampling:
            max_i = 2**MAX_TRAVERSE_NUM
        else:
            max_i = 2**self.masked_input_num

        for i in range(max_i):
            origin_output_0 = self.origin_results[
                0,
                i,
                self.origin.masked_input_num : self.origin.masked_input_num
                + self.origin.masked_output_num,
            ]

            origin_output_1 = self.origin_results[
                1,
                i,
                self.origin.masked_input_num : self.origin.masked_input_num
                + self.origin.masked_output_num,
            ]

            if (origin_output_0 == self.golden_output_results[i]).all() & (
                origin_output_1 != self.golden_output_results[i]
            ).any():
                # When target = 0, the results match.
                # When target = 1, the results don't match.
                # => target should be 0
                self.off_index.append(i)

            elif (origin_output_0 != self.golden_output_results[i]).any() & (
                origin_output_1 == self.golden_output_results[i]
            ).all():
                # When target = 0, the results don't match.
                # When target = 1, the results match.
                # => target should be 1
                self.on_index.append(i)

    def _find_candidate_base(self, node_range: list[int], levels_per_layer=2):
        """Find all possible candidate combination

        Args:
            node_num (int): The number of node in a candidate set.
        """

        # target_level = self.origin_logic_tree.target_nodes[0].level

        for node_num in node_range:
            assert node_num <= len(
                self.possible_candidate_node_index
            ), "Too many nodes."

            if (
                comb_num(len(self.possible_candidate_node_index), node_num)
                < self.comb_max
            ):
                for comb in combinations(self.possible_candidate_node_index, node_num):
                    self.iter += 1
                    self._verify_1_comb(comb)
                    if self.reach_early_stop:
                        return
            else:
                i = 0
                while not self.reach_early_stop and i < self.comb_max:
                    comb = sample(self.possible_candidate_node_index, node_num)
                    i += 1
                    self.iter += 1
                    self._verify_1_comb(comb)

            # for comb in combinations(self.possible_candidate_node_index, node_num):
            #     self.iter += 1
            #     self._verify_1_comb(comb)
            #     if self.reach_early_stop:
            #         break

    def _stratify(self, levels_per_layer=2) -> bool:
        # only support 1 target
        target_lv = self.origin.target_nodes[0].level
        self.priority_layer_num = math.floor(target_lv / levels_per_layer) + 1

        # In case only one layer
        if self.priority_layer_num == 1:
            print("Stratification failed.")
            return False

        self.priority_layers = []
        for _ in range(self.priority_layer_num):
            self.priority_layers.append([])

        # Classify all candidate into priority groups
        for node_i in self.possible_candidate_node_index:
            node = self.origin.masked_nodes[node_i]
            if node.level > target_lv:
                continue
            else:
                i = math.floor(node.level / levels_per_layer)
                self.priority_layers[i].append(node_i)

        for layer_i in range(self.priority_layer_num):
            print(f"Layer {layer_i}: ", len(self.priority_layers[layer_i]))

        return True

    def _priority_find_candidate_base(self, node_range: list[int], levels_per_layer=2):
        # priority_layer_num = 2
        #  Choose candidate comb
        for node_num in node_range:
            # print(f"Searching candidate with {node_num} inputs")

            for layer_i in list(range(1, self.priority_layer_num))[::-1]:
                if (layer_i, node_num) not in self.fully_searched:
                    if node_num <= len(self.priority_layers[layer_i]):
                        # for comb in pruned_combs(
                        #     self.priority_layers[layer_i], node_num, max=self.comb_max
                        # ):
                        #     self._verify_1_comb(comb)
                        combs, pruned = pruned_combs(
                            self.priority_layers[layer_i], node_num, max=self.comb_max
                        )

                        if not pruned:
                            print(
                                f"Layer: {layer_i}, node_num: {node_num}, has been fully searched."
                            )
                            self.fully_searched.append((layer_i, node_num))

                        self._verify_combs(combs)

                        if self.reach_early_stop:
                            return

                if (layer_i - 0.5, node_num) not in self.fully_searched:
                    # 1/2 first + 1/2 second
                    part_0 = math.ceil(node_num / 2)
                    part_1 = math.floor(node_num / 2)

                    if part_0 <= len(self.priority_layers[layer_i]) and part_1 <= len(
                        self.priority_layers[layer_i - 1]
                    ):
                        merge_combs, pruned = merge_combination(
                            self.priority_layers[layer_i],
                            part_0,
                            self.priority_layers[layer_i - 1],
                            part_1,
                            pruned_max=self.comb_max,
                        )

                        if pruned:
                            print(
                                f"Layer: {layer_i- 0.5}, node_num: {node_num}, has been fully searched."
                            )
                            self.fully_searched.append((layer_i - 0.5, node_num))
                        # for comb in merge_combs:
                        #     self._verify_1_comb(comb)
                        self._verify_combs(merge_combs)

                        if self.reach_early_stop:
                            return

    def _verify_combs(self, combs: list):
        for comb in combs:
            self.iter += 1
            self._verify_1_comb(comb)
            # if self.candidate_early_stop:
            #     return
        # temp_candidates = Manager().list()
        # self.iter += len(combs)

        # # Multiprocess
        # pool = Pool(1)
        # for comb in combs:
        #     pool.apply_async(
        #         func=sub_verify,
        #         args=(
        #             self.origin.masked_nodes,
        #             self.origin_results,
        #             self.on_index,
        #             self.off_index,
        #             comb,
        #             temp_candidates,
        #         ),
        #     )

        # pool.close()
        # pool.join()

        # self.candidate_basenodes += temp_candidates[:]

    def _verify_1_comb(self, comb):
        if not comb:
            return

        # Using numpy slice:
        result_0 = self.origin_results[0]
        on_slice = result_0[self.on_index]
        on_data_list = on_slice[:, comb]

        for i in self.off_index:
            node_comb = self.origin_results[0, i, comb]

            # if node_comb in on_data_list:
            # if np.where((node_comb == on_data_list).all(axis=1))[0].size > 0:
            if eco_ext.in_2d(on_data_list, node_comb) == 1:
                return

        base_node = BaseNode(self.origin.masked_nodes, comb, on_data_list)
        print("One pass basic verif.")

        self.candidate_basenodes.append(base_node)

    def _append_candidate(self, base_node: BaseNode):
        self.candidate_basenodes.append(base_node)
        if not self.reach_early_stop:
            self.candidate_basenodes.append(base_node)
        else:
            max_index = np.argmax(self.candidate_basenodes)
            self.candidate_basenodes[max_index] = base_node

    @property
    def reach_early_stop(self) -> bool:
        """len(self.candidate_basenodes) >= self.candidate_early_stop"""
        return len(self.candidate_basenodes) >= self.candidate_early_stop

    def print_possible_candidate(self):
        """Print all possible candidate generated by `find_candidate_base`"""

        print("All possible candidate:")
        for i, candidates in enumerate(self.candidate_basenodes):
            print(f"Candidate {i}:")
            print(candidates)

    def generate_patch(self, candidate: BaseNode) -> None:
        """Generate verilog patch of given candidate index."""
        candidate.gen_patch()

    def _input_signals(self, node_num: int) -> np.ndarray:
        """Generate input signals

        Args:
            node_num (int): signal's number

        Returns:
            list[list[int]]: For node_num=3, \n
            [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
            [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
        """
        input_signals = [list(map(int, bin(i)[2:])) for i in range(2**node_num)]

        for i in range(len(input_signals)):
            while len(input_signals[i]) < node_num:
                input_signals[i].insert(0, 0)

        return np.array(input_signals, dtype=np.int8)


def sub_verify(nodes, origin_results, on_index, off_index, comb, temp_candidates):
    result_0 = origin_results[0]
    on_slice = result_0[on_index]
    on_data_list = on_slice[:, comb]

    for i in off_index:
        node_comb = origin_results[0, i, comb]

        # if node_comb in on_data_list:
        # if np.where((node_comb == on_data_list).all(axis=1))[0].size > 0:
        if eco_ext.in_2d(on_data_list, node_comb) == 1:
            return

    base_node = BaseNode(nodes, comb, on_data_list)
    print("One pass basic verif.")
    temp_candidates.append(base_node)
