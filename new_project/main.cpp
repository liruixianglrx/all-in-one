#include "logic_tree.h"

using namespace std;

int main()
{
    LogicTree origin;
    origin.GetInputs();
    origin.PrintInputs();
    origin.forward(origin.inputs[0], vector<int>());
    // 序列化和准备阶段就绪，开始逻辑处理
    return 0;
}
