#ifndef LOGIC_TREE_H
#define LOGIC_TREE_H

#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <fstream>
#include <json.hpp>

#include <bits/stdc++.h>
#include "node.h"
#include "gate.h"

using namespace std;
class LogicTree
{
public:
    vector<Node *> node_list;
    // 记录在node_list中的index
    // TODO: masked_nodes xuliehua
    vector<int> masked_input_nodes, target_nodes, masked_output_nodes, masked_nodes;
    unordered_map<string, int> hash;
    vector<int> gate_forward_order;
    vector<Gate *> gate_list;
    vector<vector<int>> inputs;
    int masked_input_num;
    int inputs_size;
    int target_num;

public:
    LogicTree(string path)
    {
        ifstream file;
        file.open(path, ios::in);
        string tmp;
        int cnt = 0;
        if (file.is_open())
        {
            cout << "ok" << endl;
        }
        while (getline(file, tmp))
        {
            while (tmp[0] == '*')
            {
                cnt++;
                getline(file, tmp);
            }

            if (cnt == 1)
            {
                nlohmann::json json_data = nlohmann::json::parse(tmp);
                Node *tnode = new Node();
                tnode->node_name = json_data["node_name"].get<std::string>();
                tnode->level = json_data["level"].get<int>();
                tnode->value = json_data["value"].get<int>();
                json_data["driver_index"].get<int>();
                tnode->load_index = json_data["load_index"].get<std::vector<int>>();
                hash[tnode->node_name] = node_list.size();
                node_list.push_back(tnode);
            }

            if (cnt == 2)
            {
                nlohmann::json json_data = nlohmann::json::parse(tmp);
                string node_name = json_data["node_name"].get<std::string>();
                masked_input_nodes.push_back(hash[node_name]);
            }

            if (cnt == 3)
            {
                nlohmann::json json_data = nlohmann::json::parse(tmp);
                string node_name = json_data["node_name"].get<std::string>();
                target_nodes.push_back(hash[node_name]);
            }

            if (cnt == 4)
            {
                nlohmann::json json_data = nlohmann::json::parse(tmp);
                gate_forward_order = json_data.get<std::vector<int>>();
            }
            if (cnt == 5)
            {
                nlohmann::json json_data = nlohmann::json::parse(tmp);
                string gate_type = json_data["gate_type"].get<std::string>();
                vector<int> input_index = json_data["input_index"].get<std::vector<int>>();
                int output_index = json_data["output_index"].get<int>();
                Gate *gate;

                if (gate_type == "And")
                {
                    gate = new And(input_index, output_index, node_list);
                    gate->node_list = node_list;
                }
                else if (gate_type == "Not")
                {
                    gate = new Not(input_index, output_index, node_list);
                    gate->node_list = node_list;
                }
                else if (gate_type == "Buf")
                {
                    gate = new Buf(input_index, output_index, node_list);
                    gate->node_list = node_list;
                }
                else if (gate_type == "Nand")
                {
                    gate = new Nand(input_index, output_index, node_list);
                    gate->node_list = node_list;
                }
                else if (gate_type == "Or")
                {
                    gate = new Or(input_index, output_index, node_list);
                    gate->node_list = node_list;
                }
                else if (gate_type == "Nor")
                {
                    gate = new Nor(input_index, output_index, node_list);
                    gate->node_list = node_list;
                }
                else if (gate_type == "Xor")
                {
                    gate = new Xor(input_index, output_index, node_list);
                    gate->node_list = node_list;
                }
                else if (gate_type == "Xnor")
                {
                    gate = new Xnor(input_index, output_index, node_list);
                    gate->node_list = node_list;
                }

                gate_list.push_back(gate);
            }
            if (cnt == 6)
            {
                nlohmann::json json_data = nlohmann::json::parse(tmp);
                string node_name = json_data["node_name"].get<std::string>();
                masked_output_nodes.push_back(hash[node_name]);
            }
            if (cnt == 7)
            {
                masked_input_num = stoi(tmp);
            }
            if (cnt == 8)
            {
                target_num = stoi(tmp);
            }
            if (cnt == 9)
            {
                nlohmann::json json_data = nlohmann::json::parse(tmp);
                string node_name = json_data["node_name"].get<std::string>();
                masked_nodes.push_back(hash[node_name]);
            }
        }

        inputs_size = masked_input_num <= 10 ? 1 << masked_input_num : 1024;
    }

    void GetInputs()
    {
        if (masked_input_num <= 10)
        {
            std::vector<int> possible_values;
            for (int i = 0; i < (1 << masked_input_num); ++i)
            {
                decimalToBinary(i, masked_input_num, possible_values);
                inputs.push_back(possible_values);
            }
        }
        else
        {
            std::vector<int> possible_values;
            for (int i = 0; i < 1024; i++)
            {
                possible_values.clear();
                for (int j = 0; j < masked_input_num; j++)
                    possible_values.push_back(rand() % 2);
                inputs.push_back(possible_values);
            }
        }
    }

    void PrintInputs()
    {
        for (auto &input : inputs)
        {
            for (auto &it : input)
            {
                cout << it << " ";
            }
            cout << endl;
        }
    }

    void decimalToBinary(int num, int n, std::vector<int> &result)
    {
        result.clear();
        while (n > 0)
        {
            result.push_back(num % 2);
            num /= 2;
            n--;
        }
        std::reverse(result.begin(), result.end());
    }

    // in logic tree
    void forward(const std::vector<int> &input_data, const std::vector<int> &target_data)
    {
        for (int i = 0; i < masked_input_num; i++)
        {
            node_list[masked_input_nodes[i]]->value = input_data[i];
        }

        for (int i = 0; i < target_num; i++)
        {
            node_list[target_nodes[i]]->value = target_data[i];
        }

        for (int gate_index : gate_forward_order)
        {
            gate_list[gate_index]->get_output_value();
        }
    }
};

#endif