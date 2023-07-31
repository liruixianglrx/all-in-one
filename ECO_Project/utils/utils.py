import pickle
import random
from itertools import combinations, product
from math import factorial as fact
import math
from copy import deepcopy
import numpy as np


def comb_num(base: int, sample: int):
    return fact(base) / (fact(base - sample) * fact(sample))


def gen_test_vec(node_num: int) -> list[list[int]]:
    test_vec = [list(map(int, bin(i)[2:])) for i in range(2**node_num)]

    for i in range(len(test_vec)):
        while len(test_vec[i]) < node_num:
            test_vec[i].insert(0, 0)

    return test_vec


def rm_duplicates(l) -> list:
    return list(set(l))


def random_id(num: int) -> str:
    number = "0123456789"
    alpha = "abcdefghijklmnopqrstuvwxyz"

    id = ""
    for _ in range(num):
        id += random.choice(number + alpha)
    return id


def merge_combination(
    sample_list_1,
    chosen_num_1: int,
    sample_list_2,
    chosen_num_2: int,
    prune=True,
    pruned_max=2000,
) -> tuple[list, bool]:
    # combs = [list(a) + list(b) for a, b in product(comb1, comb2)]
    comb1_n = comb_num(len(sample_list_1), chosen_num_1)
    comb2_n = comb_num(len(sample_list_2), chosen_num_2)

    combs_cnt = comb1_n * comb2_n
    if prune and combs_cnt > pruned_max:
        pruned = True
        combs = []
        for _ in range(pruned_max):
            merge_comb = random.sample(sample_list_1, chosen_num_1) + random.sample(
                sample_list_2, chosen_num_2
            )
            combs.append(merge_comb)
    else:
        pruned = False
        combs = [
            list(a) + list(b)
            for a, b in product(
                combinations(sample_list_1, chosen_num_1),
                combinations(sample_list_2, chosen_num_2),
            )
        ]

    return combs, pruned


def pruned_combs(sample_list, chosen_num: int, max=2000) -> tuple[list, bool]:

    if comb_num(len(sample_list), chosen_num) > max:
        pruned = True
        combs = []
        for _ in range(max):
            combs.append(random.sample(sample_list, chosen_num))
        # combs = list(
        #     random.sample(list(combinations(sample_list, chosen_num)), chosen_max)
        # )
    else:
        pruned = False
        combs = list(combinations(sample_list, chosen_num))

    return combs, pruned


def random_input_vec(input_num: int, n: int) -> np.ndarray:
    return np.random.randint(low=0, high=2, size=(n, input_num), dtype=np.int8)


def read_pickle(pickle_path: str):
    with open(pickle_path, "rb") as f:
        data = pickle.load(f)

    return data


def relative_error(y_true, y_pred):
    return sum(np.abs(y_true - y_pred) / y_true)
