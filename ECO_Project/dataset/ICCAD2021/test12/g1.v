
// Generated by Cadence Genus(TM) Synthesis Solution 19.20-d227_1
// Generated on: Sep  7 2021 06:33:52 PDT (Sep  7 2021 13:33:52 UTC)

// Verification Directory fv/top 

module top(prim_out, sel_prim);
  input [18:0] sel_prim;
  output [31:0] prim_out;
  wire [18:0] sel_prim;
  wire [31:0] prim_out;
  wire n_0, n_1, n_2, n_3, n_4, n_5, n_6, n_7;
  wire n_8, n_9, n_10, n_11, n_12, n_13, n_14, n_15;
  wire n_16, n_17, n_18, n_19, n_20, n_21, n_22, n_24;
  wire n_25, n_26, n_27, n_28, n_29, n_30, n_31, n_33;
  wire n_34, n_35, n_36, n_37, n_38, n_39, n_40, n_44;
  wire n_45, n_46, n_47, n_48, n_49, n_52, n_53, n_55;
  wire n_57, n_58, n_59, n_61, n_63, n_64, n_65, n_66;
  wire n_67, n_68, n_69, n_70, n_71, n_72, n_73, n_74;
  wire n_76, n_77, n_78, n_573, n_786;
  assign prim_out[0] = 1'b0;
  assign prim_out[3] = 1'b1;
  not g4088 (n_78, n_77);
  not g4087 (n_76, n_77);
  assign prim_out[8] = n_77;
  not g4081 (n_74, n_69);
  and g4076 (n_73, n_63, n_64, n_65, n_71);
  and g4089 (n_72, n_35, n_37, n_34, n_71);
  not g4082 (n_70, n_69);
  and g4091 (n_77, n_47, n_10, n_68);
  nand g4090 (n_69, n_28, n_71);
  and g4102 (n_67, n_63, n_64, n_65, n_66);
  not g4099 (n_68, n_61);
  assign prim_out[14] = n_61;
  assign n_59 = n_71;
  nand g4094 (n_58, n_39, n_57);
  nand g4101 (n_61, n_48, n_57);
  and g4095 (n_71, n_66, n_57);
  assign prim_out[6] = n_57;
  not g4106 (n_55, n_57);
  not g4096 (n_53, n_52);
  not g4104 (prim_out[22], n_49);
  not g4103 (prim_out[30], n_49);
  wire w;
  nor g4109 (n_66, w, n_45);
  and g (w, sel_prim[5], n_12);
  wire w0;
  nor g4108 (n_57, w0, sel_prim[0]);
  and g0 (w0, n_38, n_48);
  and g4100 (n_52, n_47, n_17, n_33, n_46);
  nand g4107 (n_49, n_47, n_31, n_36, n_46);
  not g4114 (n_45, n_48);
  not g4115 (n_44, n_48);
  assign prim_out[5] = n_48;
  assign prim_out[2] = n_48;
  assign prim_out[4] = n_48;
  not g4110 (n_40, n_39);
  nand g4117 (n_48, sel_prim[18], n_38);
  and g4111 (n_39, n_35, n_36, n_37);
  and g4119 (n_46, n_35, n_34);
  wire w1, w2;
  and g4118 (n_33, w1, w2);
  nand g3 (w2, sel_prim[3], n_8);
  nand g1 (w1, n_25, n_30);
  nor g4122 (n_38, sel_prim[16], sel_prim[17], n_29);
  nand g4120 (n_34, sel_prim[16], n_30);
  or g4123 (n_37, sel_prim[14], sel_prim[12], n_27);
  wire w3, w4;
  nor g4124 (n_36, w3, n_22, w4);
  and g5 (w4, sel_prim[7], n_14);
  and g4 (w3, n_6, n_19);
  not g4125 (n_29, n_30);
  wire w5;
  nor g4126 (n_28, w5, n_24);
  and g6 (w5, sel_prim[2], n_11);
  nand g4129 (n_31, sel_prim[14], n_26);
  wire w6;
  nand g4130 (n_27, w6, n_26);
  or g7 (w6, sel_prim[15], n_25);
  nor g4127 (n_30, sel_prim[14], sel_prim[15], sel_prim[12], n_21);
  nor g4128 (n_24, sel_prim[12], n_64);
  not g4133 (n_22, n_65);
  not g4134 (n_26, n_21);
  nand g4135 (n_65, sel_prim[12], n_20);
  nand g4136 (n_21, n_3, n_20);
  nand g4132 (n_64, sel_prim[13], n_20);
  and g4137 (n_20, n_5, n_18, n_19);
  nand g4138 (n_17, sel_prim[11], n_18, n_19);
  nand g4140 (n_63, sel_prim[8], n_15);
  nor g4139 (n_19, sel_prim[8], n_16);
  not g4141 (n_15, n_16);
  nand g4142 (n_16, n_4, n_14);
  nor g4143 (n_14, sel_prim[5], sel_prim[6], n_13);
  not g4145 (n_13, n_12);
  nor g4146 (n_12, sel_prim[2], sel_prim[4], sel_prim[3], n_7);
  wire w7;
  nand g4144 (n_47, w7, n_11);
  or g8 (w7, sel_prim[2], n_9);
  nand g4147 (n_10, sel_prim[3], n_11);
  nor g4148 (n_9, sel_prim[3], n_2);
  nand g4149 (n_35, sel_prim[1], n_8);
  not g4151 (n_7, n_11);
  nor g4152 (n_6, sel_prim[9], n_0);
  nor g4150 (n_25, sel_prim[16], n_1);
  nor g4154 (n_11, sel_prim[0], sel_prim[1]);
  nor g4153 (n_18, sel_prim[9], sel_prim[10]);
  not g4161 (n_5, sel_prim[11]);
  not g4156 (n_4, sel_prim[7]);
  not g4157 (n_3, sel_prim[13]);
  not g4155 (n_2, sel_prim[4]);
  not g4160 (n_1, sel_prim[17]);
  not g4159 (n_0, sel_prim[10]);
  not g4158 (n_8, sel_prim[0]);
  assign prim_out[28] = n_66;
  assign prim_out[13] = n_72;
  assign prim_out[24] = n_67;
  assign prim_out[16] = n_73;
  assign prim_out[29] = n_58;
  assign prim_out[15] = n_68;
  assign prim_out[7] = n_55;
  assign prim_out[21] = n_40;
  assign prim_out[23] = n_53;
  assign prim_out[31] = n_53;
  assign prim_out[25] = n_573;
  assign prim_out[17] = n_573;
  assign prim_out[11] = n_76;
  assign prim_out[19] = n_69;
  assign prim_out[9] = n_78;
  assign prim_out[27] = n_69;
  assign prim_out[1] = n_44;
  assign prim_out[12] = n_77;
  assign prim_out[10] = n_77;
  assign prim_out[20] = n_59;
  assign prim_out[26] = n_74;
  assign prim_out[18] = n_70;
  wire w8;
  nand g2 (n_573, w8, n_786);
  or g9 (w8, n_18, n_16);
  and g4774 (n_786, n_63, n_65, n_31, n_71);
endmodule

