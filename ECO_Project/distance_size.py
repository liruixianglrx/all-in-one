import os
import pickle
from itertools import product
from multiprocessing import Manager, Pool, Process
from pprint import pprint
from random import sample

import numpy as np
from tqdm import tqdm

from utils.min_term import MinTerms
from utils.utils import *


def get_distance_size(node_num: int, minterm_num: int, result_dict: dict):
    print(f"Running: node_num: {node_num}, minterm_num: {minterm_num}")

    test_vec = gen_test_vec(node_num)

    combs = []
    for _ in range(1000):
        combs.append(sample(test_vec, minterm_num))

    for comb in tqdm(combs):
        minterm = MinTerms(comb)
        distance_sum = sum(minterm.get_distance_tuple())
        size = minterm.get_gate_num()

        if distance_sum in result_dict:
            result_dict[distance_sum].append(size)
        else:
            result_dict[distance_sum] = [size]


def comb_distance_and_size(comb: list[list[int]], result_proxy: dict, tmp_path="tmp"):
    minterm = MinTerms(comb)
    distance_sum_tuple = minterm.get_distance_tuple()
    size = minterm.get_gate_num(tmp_path=tmp_path)

    if distance_sum_tuple in result_proxy:
        result_proxy[distance_sum_tuple] += [size]
    else:
        result_proxy[distance_sum_tuple] = [size]


def get_distance_size_list(node_num: int, minterm_num: int, result_dict: dict):
    if minterm_num >= 2**node_num:
        return

    result_proxy = Manager().dict()

    test_vec = gen_test_vec(node_num)

    combs = []
    for _ in range(200):
        combs.append(sample(test_vec, minterm_num))

    pool = Pool(10)

    for i, comb in enumerate(combs):
        pool.apply_async(
            func=comb_distance_and_size, args=(comb, result_proxy, f"tmp_{i}")
        )

    pool.close()
    pool.join()

    result_dict[(node_num, minterm_num)] = result_proxy.copy()

    os.system("rm -rf tmp_*")


if __name__ == "__main__":
    # node_nums = [5, 10, 15, 20]
    # minterm_nums = [5, 10, 20, 30]
    node_nums = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15]
    minterm_nums = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 30, 40, 50]

    result_dict = dict()

    for node_num, minterm_num in tqdm(list(product(node_nums, minterm_nums))):
        get_distance_size_list(node_num, minterm_num, result_dict)

    with open(f"./size_predictor/distance_size_full.pkl", "wb") as f:
        pickle.dump(result_dict, f)
