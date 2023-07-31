import os
import pickle
import numpy as np

from tqdm import tqdm
from utils.min_term import MinTerms

from itertools import combinations
from multiprocessing import Process, Pool, Manager
from pprint import pprint
from random import sample
from math import factorial as fact


def comb_num(base: int, sample: int):
    return fact(base) / (fact(base - sample) * fact(sample))


def gen_test_vec(node_num: int) -> list[list[int]]:
    test_vec = [list(map(int, bin(i)[2:])) for i in range(2**node_num)]

    for i in range(len(test_vec)):
        while len(test_vec[i]) < node_num:
            test_vec[i].insert(0, 0)

    return test_vec


def get_dist_feat(node_num: int, minterm_num: int, tmp_path: str, result_dict: dict):

    test_vec = gen_test_vec(node_num)

    patch_size_list = []

    comb_n = comb_num(2**node_num, minterm_num)

    if comb_n < 600:
        combs = list(combinations(test_vec, minterm_num))
    else:
        combs = []
        for _ in range(300):
            combs.append(sample(test_vec, minterm_num))

    for comb in combs:
        comb = list(comb)
        patch_size_list.append(MinTerms(comb).get_gate_num(tmp_path))

    mean = float(np.mean(patch_size_list))
    std = float(np.std(patch_size_list))
    min = float(np.min(patch_size_list))
    max = float(np.max(patch_size_list))

    result_dict[minterm_num] = {
        "mean": mean,
        "std": std,
        "min": min,
        "max": max,
    }


if __name__ == "__main__":
    steps = 16
    search_range = [5, 7, 9]

    for node_num in tqdm(search_range):
        result_dict = Manager().dict()
        pool = Pool(8)

        space = ((2**node_num - 1) - 1) / 15
        minterm_range = [int(1 + space * i) for i in range(16)]

        for minterm_num in minterm_range[::-1]:
            pool.apply_async(
                func=get_dist_feat,
                args=(node_num, minterm_num, f"tmp_{minterm_num}", result_dict),
            )

        pool.close()
        pool.join()

        with open(f"./size_predictor/size_dist_{node_num}.pkl", "wb") as f:
            pickle.dump(result_dict.copy(), f)

        os.system("rm -rf tmp_*")  # clean
