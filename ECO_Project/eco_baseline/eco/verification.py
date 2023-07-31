import os

from eco_baseline.eco.base_node import BaseNode
from miter.miter import gen_miter_verilog
from copy import deepcopy

VERIF_FORMULA = """
[options]
mode prove
depth 3
vcd off

[engines]
smtbmc z3

[script]
read_verilog -formal miter.v
read_verilog G.v
read_verilog F.v
read_verilog minterm.v
prep -top miter

[files]
./tmp/miter.v
./tmp/F.v
./tmp/G.v
./tmp/minterm.v

"""


class Miter:
    def __init__(
        self,
        origin_file_path: str,
        golden_file_path: str,
        input_num: int,
        output_num: int,
    ) -> None:

        self.origin_file_path = origin_file_path
        self.input_num = input_num
        self.output_num = output_num

        with open(origin_file_path, "r") as f:
            self.origin = f.readlines()
        self.origin[0] = self.origin[0].replace("top", "F")

        with open(golden_file_path, "r") as f:
            golden = f.readlines()
        golden[0] = golden[0].replace("top", "G")

        if os.path.exists("tmp"):
            os.system("rm -rf ./tmp/*")
        else:
            os.mkdir("tmp")

        with open("./tmp/G.v", "w") as f:
            f.writelines(golden)

        gen_miter_verilog(input_width=input_num, output_width=output_num)

        with open("./tmp/verif.sby", "w") as f:
            f.writelines(VERIF_FORMULA)

    def verify(self, candidate: BaseNode, silent=True) -> bool:
        print("Miter is verifying:", candidate.simple_str)

        candidate.gen_patch()
        patch_path = "./tmp/minterm.v"

        patch_inst = "patch U_patch("
        for node in candidate.nodes_name:
            patch_inst += node + ", "
        patch_inst += "t_0); \n"

        cp_og = deepcopy(self.origin)

        cp_og.insert(-2, patch_inst)

        with open("./tmp/F.v", "w") as f:
            f.writelines(cp_og)

        if silent:
            cmd = "sby -j 8 -f ./tmp/verif.sby > /dev/null"
        else:
            cmd = "sby -j 8 -f ./tmp/verif.sby"

        if os.system(cmd) == 0:
            print("Verification Success !")
            return True
        else:
            print("Verification Fail !")
            return False
