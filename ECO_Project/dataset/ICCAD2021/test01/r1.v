module top(o, a, b, c);
output o;
input a, b, c;
AND g2(o, a, n1);
AND g1(n1, b, c);
endmodule
