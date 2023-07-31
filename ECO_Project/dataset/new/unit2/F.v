module top ( a , b , c , d, y1, y2 );
input a , b , c , d;
output y1 , y2 ;
wire w1 , w2 , w3 , w4;
wire t_0 ;

and ( w1 , a , b );
xor ( w2 , a , c );
nor ( w3 , b , c );
and ( w4 , c , d );
and ( y1 , w1 , w2 , w4);
or ( y2 , t_0 , w3 );

endmodule
