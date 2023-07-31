
// Generated by Cadence Genus(TM) Synthesis Solution 19.20-d227_1
// Generated on: Sep  7 2021 22:48:13 PDT (Sep  8 2021 05:48:13 UTC)

// Verification Directory fv/top 

module top(bitVector, adr, valid);
  input [31:0] bitVector;
  output [4:0] adr;
  output valid;
  wire [31:0] bitVector;
  wire [4:0] adr;
  wire valid;
  wire n_736, n_737, n_738, n_741, n_742, n_743, n_744, n_745;
  wire n_746, n_749, n_750, n_752, n_753, n_754, n_757, n_758;
  wire n_763, n_764, n_767, n_772, n_773, n_780, n_781, n_782;
  wire n_789, n_790, n_791, n_794, n_799, n_800, n_807, n_808;
  wire n_809, n_815, n_820, n_821, n_836, n_837, n_838, n_839;
  wire n_840, n_841, n_842, n_847, n_848, n_853, n_854, n_861;
  wire n_862, n_863, n_870, n_871, n_872, n_921, n_922, n_923;
  wire n_924, n_925, n_926, n_927, n_928, n_929, n_930, n_931;
  wire n_932, n_933, n_934, n_935, n_936, n_937, n_938, n_939;
  wire n_940, n_941, n_942, n_943, n_944, n_971, n_972, n_973;
  wire n_974, n_975, n_976, n_977, n_978, n_979, n_980, n_981;
  wire n_982, n_983;
  or g1446 (n_746, n_741, n_745);
  or g1474 (n_743, n_742, wc);
  not gc (wc, bitVector[14]);
  nand g1645 (n_758, bitVector[22], bitVector[23]);
  or g1933 (adr[0], n_944, n_754);
  or g1934 (adr[1], n_983, wc0);
  not gc0 (wc0, bitVector[30]);
  or g1935 (n_983, n_982, n_754);
  or g1936 (n_944, n_943, n_753);
  or g1937 (n_982, n_981, n_753);
  or g1938 (n_943, n_942, n_752);
  or g1939 (n_981, n_980, n_750);
  or g1940 (adr[2], n_842, n_736);
  or g1941 (n_942, n_941, wc1);
  not gc1 (wc1, n_749);
  or g1942 (n_980, n_979, n_752);
  or g1943 (n_842, n_841, wc2);
  not gc2 (wc2, n_749);
  or g1944 (n_941, n_939, n_940);
  or g1945 (n_841, n_840, n_750);
  or g1946 (n_940, n_937, n_938);
  or g1947 (n_979, n_977, n_978);
  or g1948 (n_754, n_872, wc3);
  not gc3 (wc3, bitVector[31]);
  or g1949 (n_939, n_935, n_936);
  nand g1950 (n_938, n_933, n_934);
  or g1951 (n_840, wc4, n_839);
  not gc4 (wc4, n_838);
  or g1952 (n_978, wc5, n_976);
  not gc5 (wc5, n_975);
  nand g1953 (n_872, n_870, n_871);
  nand g1954 (n_839, n_836, n_837);
  or g1955 (valid, n_863, n_746);
  or g1956 (n_975, n_746, bitVector[2]);
  or g1957 (n_870, n_746, bitVector[3]);
  nand g1958 (n_977, n_973, n_974);
  nand g1959 (n_936, n_929, n_930);
  nand g1960 (n_753, n_853, n_854);
  or g1961 (n_934, n_926, n_746);
  nand g1962 (n_976, n_971, n_972);
  or g1963 (n_929, n_921, wc6);
  not gc6 (wc6, bitVector[10]);
  or g1964 (n_854, n_745, bitVector[7]);
  nand g1965 (n_752, n_847, n_848);
  or g1966 (n_974, n_745, bitVector[6]);
  or g1967 (adr[3], n_737, wc7);
  not gc7 (wc7, n_815);
  or g1968 (n_837, wc8, n_745);
  not gc8 (wc8, n_741);
  or g1969 (n_933, n_925, n_745);
  or g1970 (n_847, n_757, bitVector[11]);
  nand g1971 (n_937, n_931, n_932);
  or g1972 (n_815, adr[4], wc9);
  not gc9 (wc9, n_744);
  nand g1973 (n_750, n_820, n_821);
  or g1974 (n_921, bitVector[9], n_757);
  or g1975 (n_745, adr[4], n_744);
  or g1976 (n_971, n_757, bitVector[10]);
  or g1977 (n_821, adr[4], bitVector[14]);
  or g1978 (n_848, adr[4], bitVector[15]);
  or g1979 (n_757, adr[4], n_743);
  or g1980 (n_836, adr[4], wc10);
  not gc10 (wc10, n_742);
  or g1981 (n_744, n_791, wc11);
  not gc11 (wc11, bitVector[10]);
  or g1982 (n_932, n_924, adr[4]);
  or g1983 (n_853, n_738, bitVector[19]);
  or g1984 (n_791, n_790, wc12);
  not gc12 (wc12, bitVector[9]);
  or g1985 (n_973, n_738, bitVector[18]);
  or g1986 (adr[4], n_809, n_738);
  or g1987 (n_931, n_923, n_738);
  nand g1988 (n_935, n_927, n_928);
  or g1989 (n_738, n_800, n_737);
  or g1990 (n_928, n_737, bitVector[23]);
  or g1991 (n_820, n_737, wc13);
  not gc13 (wc13, n_758);
  or g1992 (n_790, n_789, wc14);
  not gc14 (wc14, bitVector[11]);
  or g1993 (n_749, n_794, n_737);
  or g1994 (n_838, n_737, bitVector[20]);
  or g1995 (n_871, n_736, bitVector[27]);
  or g1996 (n_789, wc15, n_743);
  not gc15 (wc15, bitVector[8]);
  or g1997 (n_930, n_922, n_736);
  or g1998 (n_972, n_736, bitVector[26]);
  or g1999 (n_737, n_782, n_736);
  or g2000 (n_736, n_773, wc16);
  not gc16 (wc16, bitVector[30]);
  or g2001 (n_741, n_764, wc17);
  not gc17 (wc17, bitVector[6]);
  or g2002 (n_800, n_799, wc18);
  not gc18 (wc18, bitVector[20]);
  or g2003 (n_782, n_781, wc19);
  not gc19 (wc19, bitVector[26]);
  or g2004 (n_809, n_808, wc20);
  not gc20 (wc20, bitVector[18]);
  or g2005 (n_863, n_862, wc21);
  not gc21 (wc21, bitVector[2]);
  or g2006 (n_742, n_767, wc22);
  not gc22 (wc22, bitVector[15]);
  or g2007 (n_764, n_763, wc23);
  not gc23 (wc23, bitVector[7]);
  or g2008 (n_781, n_780, wc24);
  not gc24 (wc24, bitVector[25]);
  or g2009 (n_773, n_772, wc25);
  not gc25 (wc25, bitVector[31]);
  or g2010 (n_808, n_807, wc26);
  not gc26 (wc26, bitVector[19]);
  or g2011 (n_862, n_861, wc27);
  not gc27 (wc27, bitVector[1]);
  or g2012 (n_799, n_758, wc28);
  not gc28 (wc28, bitVector[21]);
  nand g2013 (n_763, bitVector[4], bitVector[5]);
  nand g2014 (n_767, bitVector[12], bitVector[13]);
  or g2015 (n_794, wc29, bitVector[21]);
  not gc29 (wc29, bitVector[22]);
  nand g2016 (n_861, bitVector[0], bitVector[3]);
  nand g2017 (n_772, bitVector[28], bitVector[29]);
  or g2018 (n_927, wc30, bitVector[29]);
  not gc30 (wc30, bitVector[30]);
  or g2019 (n_922, bitVector[25], wc31);
  not gc31 (wc31, bitVector[26]);
  nand g2020 (n_780, bitVector[24], bitVector[27]);
  or g2021 (n_923, bitVector[17], wc32);
  not gc32 (wc32, bitVector[18]);
  or g2022 (n_924, bitVector[13], wc33);
  not gc33 (wc33, bitVector[14]);
  or g2023 (n_925, bitVector[5], wc34);
  not gc34 (wc34, bitVector[6]);
  or g2024 (n_926, bitVector[1], wc35);
  not gc35 (wc35, bitVector[2]);
  nand g2025 (n_807, bitVector[16], bitVector[17]);
endmodule

