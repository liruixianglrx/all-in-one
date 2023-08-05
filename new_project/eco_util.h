#ifndef ECO_UTIL_H
#define ECO_UTIL_H

#include <vector>
#include "logic_tree.h"

vector<int> nodes_2_values(vector<int> &nodes, LogicTree *tree)
{
    vector<int> ans;
    for (auto it : nodes)
    {
        ans.push_back(tree->node_list[it]->value);
    }

    return ans;
}

#endif