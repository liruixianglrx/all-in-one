#include "logic_tree.h"
#include "eco_util.h"
#include <chrono>
using namespace std;

int main()
{
    // for golden
    LogicTree golden("/home/lrx/Desktop/all-in-one/txts/golden_logic_tree.txt");
    golden.GetInputs();

    // for origin
    LogicTree origin("/home/lrx/Desktop/all-in-one/txts/origin_logic_tree.txt");
    origin.GetInputs();

    // 运行计时
    auto start_time = std::chrono::high_resolution_clock::now();

    vector<vector<int>> golden_output_results(golden.inputs.size());
    for (int i = 0; i < golden.inputs.size(); i++)
    {
        vector<int> result;
        golden.forward(golden.inputs[i], vector<int>());
        result = nodes_2_values(golden.masked_output_nodes, &golden);
        golden_output_results[i] = result;
    }

    vector<vector<vector<int>>> origin_results(2, vector<vector<int>>(origin.inputs.size()));
    vector<vector<int>> target_inputs = {{0}, {1}};
    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < origin.inputs.size(); j++)
        {
            vector<int> result;
            origin.forward(origin.inputs[j], target_inputs[i]);
            result = nodes_2_values(origin.masked_nodes, &origin);
            origin_results[target_inputs[i][0]][j] = result;
        }
    }

    auto end_time = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count();
    std::cout << "程序运行时间：" << duration << "微秒" << std::endl;

    // 反序列化
    nlohmann::json json_obj = golden.toJson();
    std::string json_str = json_obj.dump();

    // cout << json_str << endl;

    return 0;
}
