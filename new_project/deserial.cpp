#include <iostream>
#include <string>
#include <json.hpp>
#include <bits/stdc++.h>
#include <fstream>

#include "node.h"
using namespace std;

int main() {
    // 从JSON字符串中读取数据
    ifstream file;
    file.open("/home/lrx/Desktop/test.txt",ios::in);
    string tmp;
    if (file.is_open()){
        getline(file,tmp);
    }
    std::string json_str = R"({"__type__": "Node", "node_name": "a", "level": 0, "value": -1, "driver_index": -1, "load_index": [0, 4]})";
    nlohmann::json json_data = nlohmann::json::parse(json_str);

    // 创建C++对象并从JSON数据中解析
    Node node;
    node.node_name = json_data["node_name"].get<std::string>();
    node.value = json_data["value"].get<int>();
    node.load_index = json_data["load_index"].get<std::vector<int> >();
    // for (auto &it:json_data["load_index"]) {
    //     node.load_index.push_back(it.get<int>());
    // }

    // 输出C++对象的成员
    // std::cout << "Name: " << node.node_name << std::endl;
    // std::cout << "Age: " << node.value << std::endl;
    // for (auto it : node.load_index) 
    // {
    //     cout<<it<<" ";
    // }

    cout<<node;
    return 0;
}
