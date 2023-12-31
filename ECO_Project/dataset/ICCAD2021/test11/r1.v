
// Generated by Cadence Genus(TM) Synthesis Solution 19.20-d227_1
// Generated on: Sep  7 2021 06:26:34 PDT (Sep  7 2021 13:26:34 UTC)

// Verification Directory fv/top 

module top(prim_out, sel_prim);
  input [18:0] sel_prim;
  output [31:0] prim_out;
  wire [18:0] sel_prim;
  wire [31:0] prim_out;
  wire n_723, n_725, n_728, n_732, n_734, n_736, n_739, n_742;
  wire n_746, n_748, n_749, n_753, n_759, n_793, n_796, n_826;
  wire n_828, n_831, n_833, n_834, n_835, n_836, n_839, n_842;
  wire n_847, n_848, n_853, n_854, n_863, n_864, n_865, n_866;
  wire n_869, n_874, n_875, n_882, n_883, n_884, n_889, n_890;
  wire n_895, n_896, n_903, n_904, n_905, n_914, n_915, n_916;
  wire n_917, n_926, n_927, n_928, n_929, n_932, n_939, n_940;
  wire n_941, n_944, n_947, n_956, n_957, n_958, n_959, n_966;
  wire n_967, n_968, n_971;
  assign prim_out[0] = 1'b0;
  assign prim_out[2] = prim_out[5];
  assign prim_out[3] = 1'b1;
  assign prim_out[4] = prim_out[5];
  assign prim_out[8] = prim_out[12];
  assign prim_out[9] = prim_out[11];
  assign prim_out[10] = prim_out[12];
  assign prim_out[17] = prim_out[25];
  assign prim_out[18] = prim_out[26];
  assign prim_out[19] = prim_out[27];
  assign prim_out[22] = prim_out[30];
  assign prim_out[23] = prim_out[31];
  or g167 (n_826, n_736, wc);
  not gc (wc, sel_prim[4]);
  not g171 (prim_out[1], prim_out[5]);
  or g175 (n_828, n_742, wc0);
  not gc0 (wc0, sel_prim[8]);
  or g185 (n_831, sel_prim[13], sel_prim[12]);
  or g189 (n_746, n_723, sel_prim[11]);
  or g193 (n_833, n_736, sel_prim[4]);
  or g197 (n_834, sel_prim[0], sel_prim[1]);
  or g198 (n_732, n_834, wc1);
  not gc1 (wc1, sel_prim[2]);
  or g214 (prim_out[29], prim_out[21], prim_out[7]);
  or g229 (n_835, wc2, sel_prim[0]);
  not gc2 (wc2, sel_prim[1]);
  or g235 (n_836, n_746, wc3);
  not gc3 (wc3, n_831);
  not g347 (prim_out[26], prim_out[27]);
  or g348 (prim_out[11], n_971, wc4);
  not gc4 (wc4, n_826);
  not g349 (prim_out[12], prim_out[11]);
  or g350 (prim_out[25], n_959, n_796);
  or g357 (n_971, n_734, prim_out[14]);
  or g358 (prim_out[27], n_968, n_796);
  or g359 (prim_out[14], wc5, prim_out[7]);
  not gc5 (wc5, prim_out[5]);
  not g360 (prim_out[15], prim_out[14]);
  or g361 (n_929, n_928, wc6);
  not gc6 (wc6, n_732);
  or g362 (prim_out[7], sel_prim[0], wc7);
  not gc7 (wc7, n_941);
  or g363 (n_928, n_927, wc8);
  not gc8 (wc8, n_826);
  or g364 (prim_out[31], n_917, wc9);
  not gc9 (wc9, n_739);
  or g365 (n_947, n_759, wc10);
  not gc10 (wc10, n_739);
  or g366 (n_927, n_926, wc11);
  not gc11 (wc11, n_835);
  or g367 (n_917, n_916, wc12);
  not gc12 (wc12, n_826);
  not g368 (prim_out[6], prim_out[7]);
  or g369 (n_941, n_940, wc13);
  not gc13 (wc13, prim_out[5]);
  or g372 (n_940, n_939, n_725);
  or g373 (n_916, n_915, n_728);
  or g374 (n_926, wc14, n_749);
  not gc14 (wc14, n_753);
  or g375 (n_959, n_958, wc15);
  not gc15 (wc15, n_753);
  or g376 (n_759, n_728, wc16);
  not gc16 (wc16, n_905);
  nand g377 (n_793, prim_out[5], n_932);
  or g378 (n_958, n_957, n_748);
  or g379 (n_749, n_748, wc17);
  not gc17 (wc17, n_884);
  or g380 (n_939, sel_prim[17], wc18);
  not gc18 (wc18, n_739);
  nand g381 (n_728, n_835, n_890);
  or g382 (prim_out[5], n_896, n_725);
  nand g383 (n_968, n_967, n_732);
  nand g384 (n_944, n_836, n_828);
  nand g385 (n_748, n_865, n_866);
  not g386 (prim_out[28], n_793);
  or g387 (n_890, n_889, n_725);
  or g388 (n_865, n_746, wc19);
  not gc19 (wc19, sel_prim[12]);
  or g389 (n_725, n_875, n_746);
  or g390 (n_905, n_904, n_746);
  or g391 (n_796, prim_out[7], n_793);
  or g392 (n_967, n_966, n_746);
  or g393 (n_753, n_869, n_746);
  not g394 (prim_out[20], n_796);
  or g395 (n_915, wc20, n_734);
  not gc20 (wc20, n_914);
  nand g396 (n_957, n_956, n_828);
  or g397 (n_914, n_723, wc21);
  not gc21 (wc21, sel_prim[11]);
  or g398 (n_723, n_854, n_742);
  or g399 (n_956, n_742, wc22);
  not gc22 (wc22, sel_prim[9]);
  or g400 (n_866, n_864, n_742);
  or g401 (n_742, n_848, sel_prim[5]);
  or g402 (n_884, n_883, sel_prim[5]);
  or g403 (n_848, n_847, n_833);
  or g404 (n_932, n_833, wc23);
  not gc23 (wc23, sel_prim[5]);
  or g405 (n_883, n_882, n_833);
  nand g406 (n_734, n_732, n_842);
  or g407 (n_875, n_874, sel_prim[14]);
  or g408 (n_904, n_903, sel_prim[14]);
  or g409 (n_842, n_834, wc24);
  not gc24 (wc24, sel_prim[3]);
  or g410 (n_903, wc25, n_831);
  not gc25 (wc25, sel_prim[15]);
  or g411 (n_736, n_839, n_834);
  or g412 (n_896, n_895, sel_prim[16]);
  or g413 (n_854, n_853, sel_prim[9]);
  or g414 (n_874, sel_prim[15], n_831);
  or g415 (n_864, n_863, sel_prim[8]);
  or g416 (n_966, wc26, sel_prim[12]);
  not gc26 (wc26, sel_prim[13]);
  or g417 (prim_out[21], n_759, n_749);
  or g418 (n_839, sel_prim[3], sel_prim[2]);
  or g419 (n_847, sel_prim[7], sel_prim[6]);
  or g420 (n_889, wc27, sel_prim[16]);
  not gc27 (wc27, sel_prim[17]);
  or g421 (n_853, sel_prim[10], sel_prim[8]);
  or g422 (n_863, wc28, sel_prim[9]);
  not gc28 (wc28, sel_prim[10]);
  or g423 (n_882, wc29, sel_prim[6]);
  not gc29 (wc29, sel_prim[7]);
  or g424 (n_869, wc30, sel_prim[13]);
  not gc30 (wc30, sel_prim[14]);
  or g425 (n_895, wc31, sel_prim[17]);
  not gc31 (wc31, sel_prim[18]);
  nor g426 (prim_out[24], n_944, n_793);
  and g427 (prim_out[30], wc32, n_739);
  not gc32 (wc32, n_929);
  nor g428 (prim_out[16], n_944, n_796);
  nor g429 (prim_out[13], n_947, n_796);
  or g437 (n_739, n_725, wc33);
  not gc33 (wc33, sel_prim[16]);
endmodule

