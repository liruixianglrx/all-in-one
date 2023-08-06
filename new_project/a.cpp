#include "logic_tree.h"
#include "eco_util.h"
#include <chrono>
#include <thread>
using namespace std;

int roundup(int size)
{
    if (size % 4 != 0)
        return size / 4 + 1;
    else
        return size / 4;
}
void func(LogicTree &origin, LogicTree &golden, int index)
{
    assert(origin.inputs.size() == golden.inputs.size());

    vector<vector<int>> golden_output_results(golden.inputs.size());
    int times = roundup(golden.inputs.size());
    int t2 = origin.inputs.size();
    for (int i = 0; i < times; i++)
    {
        if (i + index * times < golden.inputs.size())
        {
            vector<int> result;
            golden.forward(golden.inputs[i + index * times], vector<int>());
            result = nodes_2_values(golden.masked_output_nodes, &golden);
            golden_output_results[i + index * times] = result;
        }
    }

    vector<vector<int>> target_inputs = {{0}, {1}};
    vector<vector<vector<int>>> origin_results(2, vector<vector<int>>(origin.inputs.size()));
    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < times; j++)
        {
            if (j + index * times < golden.inputs.size())
            {
                vector<int> result;
                origin.forward(origin.inputs[j + index * times], target_inputs[i]);
                result = nodes_2_values(origin.masked_nodes, &origin);
                origin_results[target_inputs[i][0]][j + index * times] = result;
            }
        }
    }
}
int main()
{
    // for golden
    LogicTree golden("/home/lrx/Desktop/all-in-one/txts/golden_logic_tree.txt");
    golden.GetInputs();

    // for origin
    LogicTree origin("/home/lrx/Desktop/all-in-one/txts/origin_logic_tree.txt");
    origin.GetInputs();

    vector<std::thread *> threads;
    vector<vector<int>> golden_output_results(golden.inputs.size());
    vector<vector<vector<int>>> origin_results(2, vector<vector<int>>(origin.inputs.size()));

    // 运行计时
    auto start_time = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < 4; i++)
    {
        threads.push_back(new std::thread(func, std::ref(origin), std::ref(golden), i));
    }
    for (int i = 0; i < 4; i++)
    {
        threads[i]->join();
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
