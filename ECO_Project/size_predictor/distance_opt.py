import optuna
import sys
import pickle
import numpy as np

with open("distance_size_huge.pkl", "rb") as f:
    data = pickle.load(f)


def objective(trial: optuna.Trial):
    # a = trial.suggest_float("a", -1, 1)
    b = trial.suggest_float("b", 0, 2)
    # c = trial.suggest_float("c", -1, 1)

    distance_func = lambda d: b * d

    final_dict = dict()
    for k, v in data.items():
        for d_tuple, size in v.items():
            distance = sum(map(distance_func, d_tuple))
            if distance in final_dict:
                final_dict[distance] += size
            else:
                final_dict[distance] = size

    distance_list = []
    size_list = []
    for distance, size in final_dict.items():
        distance_list.append(distance)
        size_list.append(np.mean(size))

    corr = np.corrcoef(distance_list, size_list)[0, 1]

    return corr


study = optuna.create_study(
    # storage="sqlite:///distance_opt.sqlite3",
    direction="maximize",
    study_name="distance-opt",
    # load_if_exists=True,
)
study.optimize(objective, n_trials=50)
print(f"Best value: {study.best_value} (params: {study.best_params})")
