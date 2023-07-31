import math
import pickle

import numpy as np
import optuna


def get_data_wo_distance(path: str):
    with open(path, "rb") as f:
        json_data = pickle.load(f)

    X = []
    y = []

    for k, v in json_data.items():
        node_num, minterm_num = k
        for d_tuple, size in v.items():
            # distance = sum(map(distance_func, d_tuple))
            if [node_num, minterm_num] in X:
                index = X.index([node_num, minterm_num])
                y[index] += size
            else:
                X.append([node_num, minterm_num])
                y.append([np.mean(size)])

    y = list(map(lambda l: np.mean(l), y))

    X = np.array(X)
    y = np.array(y)

    return X, y


def objective(trial: optuna.Trial):
    node_3 = trial.suggest_float("node_3", -1, 5)
    node_2 = trial.suggest_float("node_2", -1, 5)
    node_1 = trial.suggest_float("node_1", -1, 5)

    minterm_2 = trial.suggest_float("minterm_2", -1, 5)
    minterm_1 = trial.suggest_float("minterm_1", -1, 5)

    size_func = (
        lambda node, min: node_3 * node**3
        + node_2 * node**2
        + node_1 * node
        + minterm_2 * min**2
        + minterm_1 * min
    )

    X, y = get_data_wo_distance("distance_size_full.pkl")

    x = [size_func(node, min) for [node, min] in X]

    corre = np.corrcoef(x, y)[0, 1]

    return corre


study = optuna.create_study(
    direction="maximize",
    storage="sqlite:///sim_predict_opt.sqlite3",
    study_name="simple predict",
    load_if_exists=True,
)
study.optimize(objective, n_trials=200)
print(f"Best value: {study.best_value} (params: {study.best_params})")
