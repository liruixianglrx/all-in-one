import os


def gen_syn_fomula(tmp_path="tmp"):
    syn_fomula = f' "read_verilog {tmp_path}/minterm.v; \
    proc; opt; techmap; opt; \
    dfflibmap -liberty syn/mycells.lib; \
    abc -liberty syn/mycells.lib; opt;\
    write_verilog -noattr {tmp_path}/synth.v; " '

    return syn_fomula


def gen_minterm(variable_list, value_table):

    # print(variable_list)

    num_of_minterms = len(value_table)
    num_of_signals = len(variable_list) - 1
    minterms = "assign " + variable_list[-1] + " = "
    for i in range(num_of_minterms):

        _this_minterm = ""

        for j in range(num_of_signals):
            if value_table[i][j] == 0:
                _this_minterm += "(!{})".format(variable_list[j])
                # pass
            elif value_table[i][j] == 1:
                _this_minterm += "({})".format(variable_list[j])

            if j != num_of_signals - 1:
                _this_minterm += "&&"

        # if value_table[i][-1] == 0:
        #    minterms += '(!({}))'.format(_this_minterm)
        # elif value_table[i][-1] == 1:
        #    minterms += '({})'.format(_this_minterm)
        if value_table[i][-1] == 1:
            minterms += "({})".format(_this_minterm)

            if i != num_of_minterms - 1:
                minterms += "||"

    minterms += ";"

    # print(minterms)

    return minterms


def yosys_flow(minterms, variable_list, tmp_path="tmp", silent=False):
    symbol = ","
    ports = symbol.join(variable_list)

    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)

    with open(f"{tmp_path}/minterm.v", "w") as f:
        f.write("module patch ({});\n".format(ports))
        for i, each in enumerate(variable_list):
            if i != len(variable_list) - 1:
                f.write("input {};\n".format(each))
            else:
                f.write("output {};\n".format(each))
        # f.write ('wire ')
        f.write(minterms)
        f.write("\n")
        f.write("endmodule")

    syn_formula = gen_syn_fomula(tmp_path)

    if silent:
        os.system(f"yosys -p {syn_formula} > /dev/null")
    else:
        os.system(f"yosys -p {syn_formula}")


if __name__ == "__main__":
    variable_list = ["g1", "g2", "t_0"]
    value_table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]

    # value_table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]

    minterms = gen_minterm(variable_list, value_table)
    print(minterms)

    yosys_flow(minterms, variable_list)
