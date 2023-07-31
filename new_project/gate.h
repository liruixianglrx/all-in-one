#include <bits/stdc++.h>

class Gate
{
public:
    Gate(const std::vector<int> &input_index, int &output_index, const std::vector<Node *> &node_list)
        : input_index(input_index), output_index(output_index),
          node_list(node_list)
    {
    }

    void set_output_value(int value)
    {
        assert(value == 0 || value == 1);
        node_list[output_index]->set_value(value);
    }

    virtual int get_output_value() = 0;

    std::vector<int> input_index;
    int output_index;
    std::string type;
    std::vector<Node *> node_list;
};

class Not : public Gate
{
public:
    Not(const std::vector<int> &input_index, int output_index, const std::vector<Node *> &node_list)
        : Gate(input_index, output_index, node_list) {}

    int get_output_value() override
    {
        int input_value = node_list[input_index[0]]->value;
        if (input_value == 1)
        {
            set_output_value(0);
            return 0;
        }
        else
        {
            set_output_value(1);
            return 1;
        }
    }
};

class Buf : public Gate
{
public:
    Buf(const std::vector<int> &input_index, int output_index, const std::vector<Node *> &node_list)
        : Gate(input_index, output_index, node_list) {}

    int get_output_value() override
    {
        int input_value = node_list[input_index[0]]->value;
        set_output_value(input_value);
        return input_value;
    }
};

class And : public Gate
{
public:
    And(const std::vector<int> &input_index, int &output_index, const std::vector<Node *> &node_list)
        : Gate(input_index, output_index, node_list) {}

    int get_output_value() override
    {
        for (int i : input_index)
        {
            if (node_list[i]->value == 0)
            {
                set_output_value(0);
                return 0;
            }
        }
        set_output_value(1);
        return 1;
    }
};

class Nand : public Gate
{
public:
    Nand(const std::vector<int> &input_index, int output_index, const std::vector<Node *> &node_list)
        : Gate(input_index, output_index, node_list) {}

    int get_output_value() override
    {
        for (int i : input_index)
        {
            if (node_list[i]->value == 0)
            {
                set_output_value(1);
                return 1;
            }
        }
        set_output_value(0);
        return 0;
    }
};

class Or : public Gate
{
public:
    Or(const std::vector<int> &input_index, int output_index, const std::vector<Node *> &node_list)
        : Gate(input_index, output_index, node_list) {}

    int get_output_value() override
    {
        for (int i : input_index)
        {
            if (node_list[i]->value == 1)
            {
                set_output_value(1);
                return 1;
            }
        }
        set_output_value(0);
        return 0;
    }
};

class Nor : public Gate
{
public:
    Nor(const std::vector<int> &input_index, int output_index, const std::vector<Node *> &node_list)
        : Gate(input_index, output_index, node_list) {}

    int get_output_value() override
    {
        for (int i : input_index)
        {
            if (node_list[i]->value == 1)
            {
                set_output_value(0);
                return 0;
            }
        }
        set_output_value(1);
        return 1;
    }
};

class Xor : public Gate
{
public:
    Xor(const std::vector<int> &input_index, int output_index, const std::vector<Node *> &node_list)
        : Gate(input_index, output_index, node_list) {}

    int get_output_value() override
    {
        int value_0 = node_list[input_index[0]]->value;
        int value_1 = node_list[input_index[1]]->value;
        if (value_0 != value_1)
        {
            set_output_value(1);
            return 1;
        }
        else
        {
            set_output_value(0);
            return 0;
        }
    }
};

class Xnor : public Gate
{
public:
    Xnor(const std::vector<int> &input_index, int output_index, const std::vector<Node *> &node_list)
        : Gate(input_index, output_index, node_list) {}

    int get_output_value() override
    {
        int value_0 = node_list[input_index[0]]->value;
        int value_1 = node_list[input_index[1]]->value;
        if (value_0 == value_1)
        {
            set_output_value(1);
            return 1;
        }
        else
        {
            set_output_value(0);
            return 0;
        }
    }
};
