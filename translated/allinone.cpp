#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <random>
#include <functional>
#include <tuple>

const int MAX_TRAVERSE_NUM = 10;

class VerilogParser {
public:
    // Implementation of VerilogParser class
};

class BaseNode {
public:
    // Implementation of BaseNode class
};

class LogicTree {
public:
    // Implementation of LogicTree class
};

class Miter {
public:
    // Implementation of Miter class
};

class Pruner {
public:
    // Implementation of Pruner class
};

class EcoEngine {
public:
    EcoEngine(std::string original_file_path, std::string golden_file_path, int early_stop = 10, bool do_pruning = true)
        : original_file_path(original_file_path),
          golden_file_path(golden_file_path),
          early_stop(early_stop),
          do_pruning(do_pruning) {
        // Constructor implementation
    }

    void run_eco(std::vector<int>& searching_node_range, bool stratified = true, int levels_per_layer = 2, int comb_max = 3000, int max_try = 10, int max_subtry = 3, int max_subsubtry = 15, bool print_mean_size = true, bool minimizing = true);

private:
    std::string original_file_path;
    std::string golden_file_path;
    int early_stop;
    bool do_pruning;
    std::vector<BaseNode> candidate_basenodes;

    void _run_traverse();
    void _traverse_golden(const std::vector<std::vector<int>>& golden_inputs);
    void _traverse_origin(const std::vector<std::vector<int>>& origin_inputs);
    void _find_on_off();
    void _find_candidate_base(std::vector<int>& node_range, int levels_per_layer);
    bool _stratify(int levels_per_layer);
    void _priority_find_candidate_base(std::vector<int>& node_range, int levels_per_layer);
    void _verify_combs(const std::vector<std::vector<int>>& combs);
    void _verify_1_comb(const std::vector<int>& comb);
    void _append_candidate(const BaseNode& base_node);
    std::tuple<BaseNode, double> _model_predict_best(const std::vector<BaseNode>& candidate_list);
    std::vector<std::vector<int>> _input_signals(int node_num);
    void generate_patch(const BaseNode& candidate);

    bool reach_early_stop() const {
        return candidate_basenodes.size() >= early_stop;
    }
};

void EcoEngine::run_eco(std::vector<int>& searching_node_range, bool stratified, int levels_per_layer, int comb_max, int max_try, int max_subtry, int max_subsubtry, bool print_mean_size, bool minimizing) {
    /* Main Process */
    int iter = 0;

    this->comb_max = comb_max;
    this->searching_node_range = searching_node_range;
    this->minimizing = minimizing;

    // Set the find function based on stratified option
    std::function<void(std::vector<int>&, int)> find_func = &EcoEngine::_find_candidate_base;
    if (stratified && _stratify(levels_per_layer)) {
        find_func = &EcoEngine::_priority_find_candidate_base;
        // To identify whether a layer has been fully searched
        fully_searched.resize(priority_layer_num, false);
    }

    if (sampling) {
        for (int try_i = 0; try_i < max_try; try_i++) {
            std::cout << "Try: " << try_i + 1 << std::endl;
            std::cout << "Node range: ";
            for (const auto& node : searching_node_range) {
                std::cout << node << " ";
            }
            std::cout << std::endl;

            std::vector<BaseNode> passed_list;
            candidate_basenodes.clear();

            int sub_try = 0;
            while (!reach_early_stop && sub_try < max_subtry) {
                sub_try++;
                std::cout << "Sub try: " << sub_try << std::endl;

                _run_traverse();
                if (!on_index.empty()) {
                    int subsub_try = 0;
                    while (!reach_early_stop && subsub_try < max_subsubtry) {
                        subsub_try++;
                        std::cout << "Subsub try: " << subsub_try << std::endl;
                        (this->*find_func)(searching_node_range, levels_per_layer);
                        if (reach_early_stop) {
                            break;
                        }
                    }
                }
                else {
                    std::cout << "No on-set" << std::endl;
                }

                if (reach_early_stop) {
                    break;
                }
            }

            for (auto& candidate : candidate_basenodes) {
                bool verify_state = miter.verify(candidate);
                if (verify_state) {
                    passed_list.push_back(candidate);
                }
            }

            if (!passed_list.empty()) {
                if (print_mean_size) {
                    double mean_size = 0.0;
                    for (const auto& b : passed_list) {
                        mean_size += b.minterms.get_gate_num();
                    }
                    mean_size /= passed_list.size();
                    std::cout << "Mean: " << mean_size << std::endl;
                }
                std::cout << "Found passed candidate" << std::endl;
                BaseNode best_candidate;
                double min_size = 1e10;
                if (minimizing) {
                    std::tie(best_candidate, min_size) = _model_predict_best(passed_list);
                }
                else {
                    best_candidate = passed_list[rand() % passed_list.size()];
                }
                std::cout << best_candidate << std::endl;
                std::cout << "ECO Success !!" << std::endl;
                std::cout << "Patch size: " << best_candidate.minterms.get_gate_num() << std::endl;
                return;
            }
            else {
                std::cout << "ECO Failed" << std::endl;
                for (auto& node : searching_node_range) {
                    node += 1;
                }
            }
        }
    }
    else {
        candidate_basenodes.clear();
        _run_traverse();
        while (!reach_early_stop) {
            (this->*find_func)(searching_node_range, levels_per_layer);
        }

        if (print_mean_size) {
            double mean_size = 0.0;
            for (const auto& b : candidate_basenodes) {
                mean_size += b.minterms.get_gate_num();
            }
            mean_size /= candidate_basenodes.size();
            std::cout << "Mean: " << mean_size << std::endl;
        }

        BaseNode best_candidate;
        double min_size = 1e10;
        if (minimizing) {
            std::tie(best_candidate, min_size) = _model_predict_best(candidate_basenodes);
            std::cout << "Smallest size: " << min_size << std::endl;
        }
        else {
            best_candidate = candidate_basenodes[rand() % candidate_basenodes.size()];
        }

        generate_patch(best_candidate);
        std::cout << "Patch: " << best_candidate << std::endl;

        if (miter.verify(best_candidate)) {
            std::cout << "ECO Success !!" << std::endl;
            std::cout << "Patch size: " << best_candidate.minterms.get_gate_num() << std::endl;
            return;
        }
    }
}

void EcoEngine::_run_traverse() {
    if (sampling) {
        std::vector<std::vector<int>> inputs = random_input_vec(masked_input_num, pow(2, MAX_TRAVERSE_NUM));
        _traverse_golden(inputs);
        _traverse_origin(inputs);
        _find_on_off();
    }
    else {
        std::vector<std::vector<int>> inputs = _input_signals(masked_input_num);
        _traverse_golden(inputs);
        _traverse_origin(inputs);
        _find_on_off();
    }
}

void EcoEngine::_traverse_golden(const std::vector<std::vector<int>>& golden_inputs) {
    golden_output_results.resize(golden_inputs.size(), std::vector<int>(golden.masked_output_num));

    for (size_t i = 0; i < golden_inputs.size(); i++) {
        golden.forward(golden_inputs[i], []);
        std::vector<int> result = eco_utils.nodes_2_values(golden.masked_output_nodes);
        golden_output_results[i] = result;
    }
}

void EcoEngine::_traverse_origin(const std::vector<std::vector<int>>& origin_inputs) {
    origin_results.resize(2, std::vector<std::vector<int>>(origin_inputs.size(), std::vector<int>(origin.masked_node_num)));

    std::vector<std::vector<int>> target_inputs = {{0}, {1}};

    for (size_t target_i = 0; target_i < target_inputs.size(); target_i++) {
        std::vector<std::vector<int>>& results_of_one_target = origin_results[target_inputs[target_i][0]];
        for (size_t i = 0; i < origin_inputs.size(); i++) {
            origin.forward(origin_inputs[i], target_inputs[target_i]);
            std::vector<int> result = eco_utils.nodes_2_values(origin.masked_nodes);
            results_of_one_target[i] = result;
        }
    }
}

void EcoEngine::_find_on_off() {
    on_index.clear();
    off_index.clear();

    int max_i = sampling ? pow(2, MAX_TRAVERSE_NUM) : pow(2, masked_input_num);

    for (int i = 0; i < max_i; i++) {
        std::vector<int> origin_output_0 = origin_results[0][i].subspan(masked_input_num, origin.masked_output_num);
        std::vector<int> origin_output_1 = origin_results[1][i].subspan(masked_input_num, origin.masked_output_num);

        bool match_0 = std::equal(origin_output_0.begin(), origin_output_0.end(), golden_output_results[i].begin());
        bool match_1 = std::equal(origin_output_1.begin(), origin_output_1.end(), golden_output_results[i].begin());

        if (match_0 && !match_1) {
            off_index.push_back(i);
        }
        else if (!match_0 && match_1) {
            on_index.push_back(i);
        }
    }
}

void EcoEngine::_find_candidate_base(std::vector<int>& node_range, int levels_per_layer) {
    for (int node_num : node_range) {
        assert(node_num <= possible_candidate_node_index.size());
        if (comb_num(possible_candidate_node_index.size(), node_num) < comb_max) {
            std::vector<int> comb;
            do {
                comb = next_combination();
                iter++;
                _verify_1_comb(comb);
                if (reach_early_stop) {
                    return;
                }
            } while (!comb.empty());
        }
        else {
            int i = 0;
            while (!reach_early_stop && i < comb_max) {
                std::vector<int> comb = sample_combination(node_num);
                i++;
                iter++;
                _verify_1_comb(comb);
            }
        }
    }
}

bool EcoEngine::_stratify(int levels_per_layer) {
    int target_lv = origin.target_nodes[0].level;
    priority_layer_num = std::floor(target_lv / levels_per_layer) + 1;

    if (priority_layer_num == 1) {
        std::cout << "Stratification failed." << std::endl;
        return false;
    }

    priority_layers.resize(priority_layer_num);

    for (int node_i : possible_candidate_node_index) {
        const BaseNode& node = origin.masked_nodes[node_i];
        if (node.level > target_lv) {
            continue;
        }
        else {
            int i = std::floor(node.level / levels_per_layer);
            priority_layers[i].push_back(node_i);
        }
    }

    for (int layer_i = 0; layer_i < priority_layer_num; layer_i++) {
        std::cout << "Layer " << layer_i << ": ";
        for (int node_i : priority_layers[layer_i]) {
            std::cout << node_i << " ";
        }
        std::cout << std::endl;
    }

    return true;
}

void EcoEngine::_priority_find_candidate_base(std::vector<int>& node_range, int levels_per_layer) {
    for (int layer_i = 0; layer_i < priority_layer_num; layer_i++) {
        std::vector<int>& layer_nodes = priority_layers[layer_i];

        if (layer_i < fully_searched.size() && fully_searched[layer_i]) {
            continue;
        }

        for (int node_num : node_range) {
            assert(node_num <= layer_nodes.size());
            if (comb_num(layer_nodes.size(), node_num) < comb_max) {
                std::vector<int> comb;
                do {
                    comb = next_combination(layer_nodes);
                    iter++;
                    _verify_1_comb(comb);
                    if (reach_early_stop) {
                        return;
                    }
                } while (!comb.empty());
            }
            else {
                int i = 0;
                while (!reach_early_stop && i < comb_max) {
                    std::vector<int> comb = sample_combination(layer_nodes, node_num);
                    i++;
                    iter++;
                    _verify_1_comb(comb);
                }
            }
        }

        if (layer_i < fully_searched.size()) {
            fully_searched[layer_i] = true;
        }
    }
}

void EcoEngine::_verify_combs(const std::vector<std::vector<int>>& combs) {
    for (const std::vector<int>& comb : combs) {
        _verify_1_comb(comb);
        if (reach_early_stop) {
            return;
        }
    }
}

void EcoEngine::_verify_1_comb(const std::vector<int>& comb) {
    if (comb.empty()) {
        return;
    }

    std::vector<int> on_masked_inputs = origin.get_input_by_index(on_index);
    std::vector<int> off_masked_inputs = origin.get_input_by_index(off_index);

    std::vector<int> on_outputs = origin.get_output_by_index(on_index);
    std::vector<int> off_outputs = origin.get_output_by_index(off_index);

    std::vector<int> on_outputs_diff = eco_utils.calc_diff(golden_output_results, on_outputs);
    std::vector<int> off_outputs_diff = eco_utils.calc_diff(golden_output_results, off_outputs);

    bool can_prune = false;
    if (do_pruning) {
        can_prune = pruner.prune(comb, on_outputs_diff, off_outputs_diff);
    }

    if (!can_prune) {
        std::vector<int> all_inputs = on_masked_inputs;
        all_inputs.insert(all_inputs.end(), off_masked_inputs.begin(), off_masked_inputs.end());

        LogicTree tree;
        tree.build(comb, all_inputs, on_outputs_diff, off_outputs_diff);

        BaseNode base_node(tree);
        base_node.minterms = tree.get_minterms();

        _append_candidate(base_node);
    }
}

void EcoEngine::_append_candidate(const BaseNode& base_node) {
    candidate_basenodes.push_back(base_node);
    if (reach_early_stop()) {
        reach_early_stop = true;
    }
}

std::tuple<BaseNode, double> EcoEngine::_model_predict_best(const std::vector<BaseNode>& candidate_list) {
    BaseNode best_candidate;
    double min_size = 1e10;

    for (const BaseNode& candidate : candidate_list) {
        double size = candidate.minterms.get_gate_num();
        if (size < min_size) {
            best_candidate = candidate;
            min_size = size;
        }
    }

    return std::make_tuple(best_candidate, min_size);
}

std::vector<std::vector<int>> EcoEngine::_input_signals(int node_num) {
    std::vector<std::vector<int>> inputs;

    int input_comb_num = pow(2, node_num);
    inputs.resize(input_comb_num);

    for (int i = 0; i < input_comb_num; i++) {
        std::vector<int> input_signals;
        int num = i;
        for (int j = 0; j < node_num; j++) {
            input_signals.push_back(num % 2);
            num = num / 2;
        }
        inputs[i] = input_signals;
    }

    return inputs;
}

void EcoEngine::generate_patch(const BaseNode& candidate) {
    // Patch generation logic
    // ...
}

int main() {
    std::string original_file_path = "path/to/original/file";
    std::string golden_file_path = "path/to/golden/file";

    std::vector<int> searching_node_range = {1, 2, 3};

    EcoEngine ecoEngine(original_file_path, golden_file_path);
    ecoEngine.run_eco(searching_node_range);

    return 0;
}

