import os


def gen_miter_verilog(input_width, output_width):
    # generate miter file
    if os.path.exists("./tmp/miter.v"):
        os.system("rm ./tmp/miter.v")
    file_miter = open("./tmp/miter.v", "a")

    # write body
    file_miter.write("module miter(input [{}:0] a, o);\n".format(input_width - 1))
    file_miter.write("wire [{}:0] out_f;\n".format(output_width - 1))
    file_miter.write("wire [{}:0] out_g;\n".format(output_width - 1))
    f_ports = ""
    for i in range(input_width):
        f_ports += "a[{}], ".format(i)
    for i in range(output_width):
        f_ports += "out_f[{}], ".format(i)

    f_ports = f_ports[:-2]
    file_miter.write("F f({})".format(f_ports))
    file_miter.write(";\n")

    #
    g_ports = ""
    for i in range(input_width):
        g_ports += "a[{}], ".format(i)
    for i in range(output_width):
        g_ports += "out_g[{}], ".format(i)
    g_ports = g_ports[:-2]
    file_miter.write("G g({})".format(g_ports))
    file_miter.write(";\n")

    file_miter.write("wire [{}:0] verif;\n".format(output_width - 1))

    file_miter.write("genvar i;\n")
    file_miter.write("generate\n")
    file_miter.write("for(i = 0; i < {}; i = i + 1)\n".format(output_width))
    file_miter.write("assign verif[i] = out_f[i] ^ out_g[i];\n")
    file_miter.write("endgenerate\n")
    file_miter.write("assign o = |verif;\n")
    file_miter.write("`ifdef FORMAL\nalways @* assert (o == 0);\n`endif\n")
    file_miter.write("endmodule")


if __name__ == "__main__":
    gen_miter_verilog(3, 2)
