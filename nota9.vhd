LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_SIGNED.ALL;
PACKAGE PARAMETERS IS
CONSTANT n: NATURAL := 10;
CONSTANT inv_sqrt_2: SIGNED(n-1 DOWNTO 0) := "00"&x"B5";
TYPE Q_STATE IS ARRAY (NATURAL RANGE <>) OF SIGNED(n-1 DOWNTO 0);
END PACKAGE;

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_SIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY FP_MUL IS
   PORT(
      A, B: IN SIGNED(n-1 DOWNTO 0);
      C: OUT SIGNED(n-1 DOWNTO 0)
      );
END FP_MUL;

ARCHITECTURE CIRCUIT OF FP_MUL IS
   SIGNAL long_A, long_B: SIGNED(2*n-1 DOWNTO 0); 
   SIGNAL long_C: SIGNED(4*n-1 DOWNTO 0);   
BEGIN
   long_A(2*n-1 DOWNTO n)<= (OTHERS => A(n-1));
   long_A(n-1 DOWNTO 0)<= A;
   long_B(2*n-1 DOWNTO n)<= (OTHERS => B(n-1));
   long_B(n-1 DOWNTO 0)<= B;
 
   long_C <=  long_A*long_B;
   C <= long_C(2*n-3 DOWNTO n-2);

END CIRCUIT;

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY H_gate IS
PORT(
 S, T: IN Q_STATE(0 TO 7);
 Next_S, Next_T: OUT Q_STATE(0 TO 7)
);
END H_gate;
 
ARCHITECTURE circuit OF H_gate IS
 COMPONENT FP_MUL IS
   PORT(
      A, B: IN SIGNED(n-1 DOWNTO 0);
      C: OUT SIGNED(n-1 DOWNTO 0)
      );
   END COMPONENT; 
  SIGNAL S1, T1: Q_STATE(0 TO 7);  
BEGIN
   steps: FOR i IN 0 TO 3 GENERATE
      S1(i) <= S(i) + S(i+4); T1(i) <= T(i) + T(i+4);
      S1(i+4) <= S(i) - S(i+4); T1(i+4) <= T(i) - T(i+4);
      multiplier1: FP_MUL PORT MAP(A => S1(i), B => inv_sqrt_2, C => Next_S(i));
      multiplier2: FP_MUL PORT MAP(A => S1(4+i), B => inv_sqrt_2, C => Next_S(4+i));
      multiplier3: FP_MUL PORT MAP(A => T1(i), B => inv_sqrt_2, C => Next_T(i));
      multiplier4: FP_MUL PORT MAP(A => T1(4+i), B => inv_sqrt_2, C => Next_T(4+i));
   END GENERATE;
END circuit;

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY TEST_H_gate IS
END TEST_H_gate; 


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY H_gate_1 IS
PORT(
 S, T: IN Q_STATE(0 TO 7);
 Next_S, Next_T: OUT Q_STATE(0 TO 7)
);
END H_gate_1;
 
ARCHITECTURE circuit OF H_gate_1 IS
 COMPONENT FP_MUL IS
   PORT(
      A, B: IN SIGNED(n-1 DOWNTO 0);
      C: OUT SIGNED(n-1 DOWNTO 0)
      );
   END COMPONENT; 
  SIGNAL S1, T1: Q_STATE(0 TO 7);  
BEGIN
   S1(0) <= S(0) + S(2) ; T1(0) <= T(0) + T(2);     
   S1(1) <= S(1) + S(3) ; T1(1) <= T(1) + T(3);     
   S1(2) <= S(0) - S(2) ; T1(2) <= T(0) - T(2);     
   S1(3) <= S(1) - S(3) ; T1(3) <= T(1) - T(3);
   S1(4) <= S(4) + S(6) ; T1(4) <= T(4) + T(6);     
   S1(5) <= S(5) + S(7) ; T1(5) <= T(5) + T(7); 
   S1(6) <= S(4) - S(6) ; T1(6) <= T(4) - T(6); 
   S1(7) <= S(5) - S(7) ; T1(7) <= T(5) - T(7); 
   components: FOR i IN 0 TO 7 GENERATE
      BEGIN
      multiplier1: FP_MUL PORT MAP(A => S1(i), B => inv_sqrt_2, C => Next_S(i));
      multiplier2: FP_MUL PORT MAP(A => T1(i), B => inv_sqrt_2, C => Next_T(i));
   END GENERATE;
END circuit;

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY H_gate_2 IS
PORT(
 S, T: IN Q_STATE(0 TO 7);
 Next_S, Next_T: OUT Q_STATE(0 TO 7)
);
END H_gate_2;
 
ARCHITECTURE circuit OF H_gate_2 IS
 COMPONENT FP_MUL IS
   PORT(
      A, B: IN SIGNED(n-1 DOWNTO 0);
      C: OUT SIGNED(n-1 DOWNTO 0)
      );
   END COMPONENT; 
  SIGNAL S1, T1: Q_STATE(0 TO 7);  
BEGIN
   S1(0) <= S(0) + S(1) ; T1(0) <= T(0) + T(1);     
   S1(1) <= S(0) - S(1) ; T1(1) <= T(0) - T(1);     
   S1(2) <= S(2) + S(3) ; T1(2) <= T(2) + T(3);     
   S1(3) <= S(2) - S(3) ; T1(3) <= T(2) - T(3);
   S1(4) <= S(4) + S(5) ; T1(4) <= T(4) + T(5);     
   S1(5) <= S(4) - S(5) ; T1(5) <= T(4) - T(5); 
   S1(6) <= S(6) + S(7) ; T1(6) <= T(6) + T(7); 
   S1(7) <= S(6) - S(7) ; T1(7) <= T(6) - T(7); 
   components: FOR i IN 0 TO 7 GENERATE
      BEGIN
      multiplier1: FP_MUL PORT MAP(A => S1(i), B => inv_sqrt_2, C => Next_S(i));
      multiplier2: FP_MUL PORT MAP(A => T1(i), B => inv_sqrt_2, C => Next_T(i));
   END GENERATE;
END circuit;


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY CX_01 IS
PORT(
 S, T: IN Q_STATE(0 TO 7);
 Next_S, Next_T: OUT Q_STATE(0 TO 7)
);
END CX_01;
 
ARCHITECTURE circuit OF CX_01 IS 
BEGIN
   Next_S(0) <= S(0) ; Next_T(0) <= T(0);     
   Next_S(1) <= S(1) ; Next_T(1) <= T(1);     
   Next_S(2) <= S(2) ; Next_T(2) <= T(2);     
   Next_S(3) <= S(3) ; Next_T(3) <= T(3);
   Next_S(4) <= S(6) ; Next_T(4) <= T(6);     
   Next_S(5) <= S(7) ; Next_T(5) <= T(7);     
   Next_S(6) <= S(4) ; Next_T(6) <= T(4);     
   Next_S(7) <= S(5) ; Next_T(7) <= T(5);
END circuit;


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY CR_PI_2_10 IS
PORT(
 S, T: IN Q_STATE(0 TO 7);
 Next_S, Next_T: OUT Q_STATE(0 TO 7)
);
END CR_PI_2_10;
 
ARCHITECTURE circuit OF CR_PI_2_10 IS 
 COMPONENT FP_MUL IS
   PORT(
      A, B: IN SIGNED(n-1 DOWNTO 0);
      C: OUT SIGNED(n-1 DOWNTO 0)
      );
   END COMPONENT; 
BEGIN
   Next_S(0) <= S(0) ; Next_T(0) <= T(0);     
   Next_S(1) <= S(1) ; Next_T(1) <= T(1);     
   Next_S(2) <= S(2) ; Next_T(2) <= T(2);     
   Next_S(3) <= S(3) ; Next_T(3) <= T(3);
   Next_S(4) <= S(4) ; Next_T(4) <= T(4);     
   Next_S(5) <= S(5) ; Next_T(5) <= T(5); 
   Next_S(6) <= -T(6) ; Next_T(6) <= S(6); 
   Next_S(7) <= -T(7) ; Next_T(7) <= S(7); 
END circuit;


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY CR_PI_2_21 IS
PORT(
 S, T: IN Q_STATE(0 TO 7);
 Next_S, Next_T: OUT Q_STATE(0 TO 7)
);
END CR_PI_2_21;
 
ARCHITECTURE circuit OF CR_PI_2_21 IS 
 COMPONENT FP_MUL IS
   PORT(
      A, B: IN SIGNED(n-1 DOWNTO 0);
      C: OUT SIGNED(n-1 DOWNTO 0)
      );
   END COMPONENT; 
BEGIN
   Next_S(0) <= S(0) ; Next_T(0) <= T(0);     
   Next_S(1) <= S(1) ; Next_T(1) <= T(1);     
   Next_S(2) <= S(2) ; Next_T(2) <= T(2);     
   Next_S(3) <= -T(3) ; Next_T(3) <= S(3);
   Next_S(4) <= S(4) ; Next_T(4) <= T(4);     
   Next_S(5) <= S(5) ; Next_T(5) <= T(5); 
   Next_S(6) <= S(6) ; Next_T(6) <= T(6); 
   Next_S(7) <= -T(7) ; Next_T(7) <= S(7); 
END circuit;


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY CR_PI_4_20 IS
PORT(
 S, T: IN Q_STATE(0 TO 7);
 Next_S, Next_T: OUT Q_STATE(0 TO 7)
);
END CR_PI_4_20;
 
ARCHITECTURE circuit OF CR_PI_4_20 IS 
 COMPONENT FP_MUL IS
   PORT(
      A, B: IN SIGNED(n-1 DOWNTO 0);
      C: OUT SIGNED(n-1 DOWNTO 0)
      );
   END COMPONENT; 
   SIGNAL S5, T5, S7, T7: SIGNED(9 DOWNTO 0);
BEGIN
   Next_S(0) <= S(0) ; Next_T(0) <= T(0);     
   Next_S(1) <= S(1) ; Next_T(1) <= T(1);     
   Next_S(2) <= S(2) ; Next_T(2) <= T(2);     
   Next_S(3) <= S(3) ; Next_T(3) <= T(3);
   Next_S(4) <= S(4) ; Next_T(4) <= T(4);     
   Next_S(6) <= -T(6) ; Next_T(6) <= S(6); 
   S5 <= S(5)-T(5) ; T5 <= S(5) + T(5); 
   component1: FP_MUL PORT MAP (S5, inv_sqrt_2, Next_S(5));
   component2: FP_MUL PORT MAP (T5, inv_sqrt_2, Next_T(5));
   S7 <= S(7)-T(7) ; T7 <= S(7) + T(7); 
   component3: FP_MUL PORT MAP (S7, inv_sqrt_2, Next_S(7));
   component4: FP_MUL PORT MAP (T7, inv_sqrt_2, Next_T(7));
END circuit;


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY QFT_3 IS
PORT(
 S, T: IN Q_STATE(0 TO 7);
 Next_S, Next_T: OUT Q_STATE(0 TO 7)
);
END QFT_3;
 
ARCHITECTURE circuit OF QFT_3 IS 
   COMPONENT H_gate IS
     PORT(
     S, T: IN Q_STATE(0 TO 7);
     Next_S, Next_T: OUT Q_STATE(0 TO 7)
    ); 
   END COMPONENT; 
   COMPONENT H_gate_1 IS
     PORT(
     S, T: IN Q_STATE(0 TO 7);
     Next_S, Next_T: OUT Q_STATE(0 TO 7)
    ); 
   END COMPONENT; 
   COMPONENT H_gate_2 IS
     PORT(
     S, T: IN Q_STATE(0 TO 7);
     Next_S, Next_T: OUT Q_STATE(0 TO 7)
    ); 
   END COMPONENT; 
   COMPONENT CR_PI_2_10 IS
     PORT(
     S, T: IN Q_STATE(0 TO 7);
     Next_S, Next_T: OUT Q_STATE(0 TO 7)
    ); 
   END COMPONENT; 
   COMPONENT CR_PI_4_20 IS
     PORT(
     S, T: IN Q_STATE(0 TO 7);
     Next_S, Next_T: OUT Q_STATE(0 TO 7)
    ); 
   END COMPONENT; 
   COMPONENT CR_PI_2_21 IS
     PORT(
     S, T: IN Q_STATE(0 TO 7);
     Next_S, Next_T: OUT Q_STATE(0 TO 7)
    ); 
   END COMPONENT; 
   SIGNAL S1, T1, S2, T2, S3, T3, S4, T4, S5, T5, S7, T7: Q_STATE(0 TO 7);
BEGIN
   component1: H_gate PORT MAP (S, T, S1, T1);
   component2: CR_PI_2_10 PORT MAP (S1, T1, S2, T2);
   component3: CR_PI_4_20 PORT MAP (S2, T2, S3, T3);
   component4: H_gate_1  PORT MAP (S3, T3, S4, T4);
   component5: CR_PI_2_21 PORT MAP (S4, T4, S5, T5);   
   component6: H_gate_2 PORT MAP (S5, T5, Next_S,Next_T);
END circuit;

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY TEST_QFT_3 IS
END TEST_QFT_3;

ARCHITECTURE circuit OF TEST_QFT_3 IS
   COMPONENT QFT_3 IS
   PORT(
   S, T: IN Q_STATE(0 TO 7);
   Next_S, Next_T: OUT Q_STATE(0 TO 7)
   );
   END COMPONENT;
   SIGNAL S, T, Next_S, Next_T: Q_STATE(0 TO 7);
BEGIN
   dut: QFT_3 PORT MAP(S, T, Next_S, Next_T);
   S <= ("00"&x"00", "00"&x"00","00"&x"00","00"&x"00","00"&x"00","01"&x"00","00"&x"00","00"&x"00"),
   ("00"&x"00", "00"&x"00","00"&x"00","00"&x"00","01"&x"00","00"&x"00","00"&x"00","00"&x"00") after 500 ns,
   ("00"&x"00", "00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00") after 1000 ns;
   T <= ("00"&x"00", "00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00"),
   ("01"&x"00", "00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00") after 1000 ns;  
END circuit;


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY Bell_states IS
PORT(
 S, T: IN Q_STATE(0 TO 7);
 Next_S, Next_T: OUT Q_STATE(0 TO 7)
);
END Bell_states;
 
ARCHITECTURE circuit OF Bell_states IS 
   COMPONENT H_gate IS
     PORT(
     S, T: IN Q_STATE(0 TO 7);
     Next_S, Next_T: OUT Q_STATE(0 TO 7)
    ); 
   END COMPONENT; 
  COMPONENT CX_01 IS
    PORT(
    S, T: IN Q_STATE(0 TO 7);
    Next_S, Next_T: OUT Q_STATE(0 TO 7)
    );
   END COMPONENT;
   SIGNAL S1, T1: Q_STATE(0 TO 7);
BEGIN
   first: H_gate PORT MAP (S, T, S1, T1);
   second: CX_01 PORT MAP (S1, T1, Next_S, Next_T);
END circuit;

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY TEST_Bell_states IS
END TEST_Bell_states; 
ARCHITECTURE TEST OF TEST_Bell_states  IS
   COMPONENT Bell_states IS
   PORT(
   S, T: IN Q_STATE(0 TO 7);
   Next_S, Next_T: OUT Q_STATE(0 TO 7)
   );
   END COMPONENT;
   SIGNAL S, T, Next_S, Next_T: Q_STATE(0 TO 7);
BEGIN
   dut: Bell_states PORT MAP (S => S, T => T, Next_S => Next_S, Next_T => Next_T);
   S <= ("01"&x"00", "00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00"),
        ("00"&x"00", "00"&x"00","00"&x"00","00"&x"00","01"&x"00","00"&x"00","00"&x"00","00"&x"00") after 1000 ns,
        ("00"&x"00", "00"&x"00","01"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00") after 2000 ns,
        ("00"&x"00", "00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","01"&x"00","00"&x"00") after 3000 ns;
   T <= ("00"&x"00", "00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00","00"&x"00");
END TEST;

