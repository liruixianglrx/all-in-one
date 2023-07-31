module top ( a , b , c , d , y1, y2 );
input a , b , c , d;
output y1 , y2 ;
wire w1 , w2 , w3 , w4 , w5;

not ( w1 , c );
and ( w2 , a , w1 );
nor ( w3 , a , b );
and ( w4 , b , c );
and ( w5 , c , d );
and ( y1 , b , w2 , w5);
or ( y2 , w2 , w3 , w4 );

endmodule
