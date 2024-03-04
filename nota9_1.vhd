LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_SIGNED.ALL;
PACKAGE PARAMETERS IS
CONSTANT n: NATURAL := 10;
CONSTANT inv_sqrt_2: SIGNED(n-1 DOWNTO 0) := "00"&x"B5";
CONSTANT minus_inv_sqrt_2: SIGNED(n-1 DOWNTO 0) := "11"&x"4B";
CONSTANT zero: SIGNED(n-1 DOWNTO 0) := "00"&x"00";
CONSTANT one: SIGNED(n-1 DOWNTO 0) := "01"&x"00";
CONSTANT minus_one: SIGNED(n-1 DOWNTO 0) := "11"&x"00";
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
USE IEEE.STD_LOGIC_SIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY FP_MUL_ADD IS
   PORT(
      X, Y, A, B: IN SIGNED(n-1 DOWNTO 0);
      C: OUT SIGNED(n-1 DOWNTO 0)
      );
END FP_MUL_ADD;

ARCHITECTURE CIRCUIT OF FP_MUL_ADD IS
   COMPONENT FP_MUL IS   
   PORT(
      A, B: IN SIGNED(n-1 DOWNTO 0);
      C: OUT SIGNED(n-1 DOWNTO 0)
      );
   END COMPONENT;
   SIGNAL AX, BY: SIGNED(n-1 DOWNTO 0);
BEGIN
   mul1: FP_MUL PORT MAP(A => A, B=> X, C => AX);
   mul2: FP_MUL PORT MAP(A => B, B=> Y, C => BY);
   C <= AX +BY;
END CIRCUIT;


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE WORK.PARAMETERS.ALL;
ENTITY QFT_3 IS
PORT(
 clk, reset: IN STD_LOGIC;
 S_out, T_out: OUT Q_STATE(0 TO 7)
);
END QFT_3;
 
ARCHITECTURE circuit OF QFT_3 IS 
   COMPONENT FP_MUL_ADD IS
   PORT(
      X, Y, A, B: IN SIGNED(n-1 DOWNTO 0);
      C: OUT SIGNED(n-1 DOWNTO 0)
      );
   END COMPONENT;
   SIGNAL S, T, Next_S, Next_T, V, VV, W, WW, C, D, CC, DD: Q_STATE(0 TO 7); 
   TYPE step IS RANGE 0 TO 7;
   SIGNAL current_step: step;
BEGIN

--DATA PATH
   state_register: PROCESS (clk, reset, Next_S, Next_T)
   BEGIN
      IF reset = '1' THEN         
         FOR i IN 0 TO 4 LOOP
         S(i) <= "00"&x"00"; T(i) <= "00"&x"00";
         END LOOP;
         S(5) <= "01"&x"00"; T(5) <= "00"&x"00";
         S(6) <= "00"&x"00"; T(6) <= "00"&x"00";
         S(7) <= "00"&x"00"; T(7) <= "00"&x"00";
       ELSIF clk'event AND clk = '1' THEN 
         S <= Next_S; T <= Next_T;
       END IF;
   END PROCESS;
   S_out <= S; T_out <= T;
   computation_resources: FOR k IN 0 TO 7 GENERATE
      comp1: FP_MUL_ADD PORT MAP(X => V(k) , Y => W(k), A => C(k) , B => D(k), C => Next_S(k));
      comp2: FP_MUL_ADD PORT MAP(X => VV(k), Y => WW(k), A => CC(k), B => DD(k), C => Next_T(k));
   END GENERATE;

--CONTROL UNIT
   steps: PROCESS (clk, reset)
   BEGIN
   IF reset = '1' THEN current_step <= 0;
   ELSIF clk'event AND clk = '1' THEN
      CASE current_step IS
         WHEN 0 => current_step <= 1;
         WHEN 1 => current_step <= 2;
         WHEN 2 => current_step <= 3;
         WHEN 3 => current_step <= 4;
         WHEN 4 => current_step <= 5;
         WHEN 5 => current_step <= 6;
         WHEN 6 => current_step <= 7;
         WHEN 7 => current_step <= 7;
      END CASE;
   END IF;
   END PROCESS;

   connections: PROCESS (current_step, S, T)
   BEGIN
   CASE current_step IS
   WHEN 0 => 
   -- NOP
   V(0) <= S(0); W(0) <= zero; C(0) <= one; D(0) <= zero; 
   VV(0) <= T(0); WW(0) <= zero; CC(0) <= one; DD(0) <= zero; 
   V(1) <= S(1); W(1) <= zero; C(1) <= one; D(1) <= zero; 
   VV(1) <= T(1); WW(1) <= zero; CC(1) <= one; DD(1) <= zero; 
   V(2) <= S(2); W(2) <= zero; C(2) <= one; D(2) <= zero; 
   VV(2) <= T(2); WW(2) <= zero; CC(2) <= one; DD(2) <= zero; 
   V(3) <= S(3); W(3) <= zero; C(3) <= one; D(3) <= zero; 
   VV(3) <= T(3); WW(3) <= zero; CC(3) <= one; DD(3) <= zero; 
   V(4) <= S(4); W(4) <= zero; C(4) <= one; D(4) <= zero; 
   VV(4) <= T(4); WW(4) <= zero; CC(4) <= one; DD(4) <= zero; 
   V(5) <= S(5); W(5) <= zero; C(5) <= one; D(5) <= zero; 
   VV(5) <= T(5); WW(5) <= zero; CC(5) <= one; DD(5) <= zero; 
   V(6) <= S(6); W(6) <= zero; C(6) <= one; D(6) <= zero; 
   VV(6) <= T(6); WW(6) <= zero; CC(6) <= one; DD(6) <= zero; 
   V(7) <= S(7); W(7) <= zero; C(7) <= one; D(7) <= zero; 
   VV(7) <= T(7); WW(7) <= zero; CC(7) <= one; DD(7) <= zero;
   WHEN 1 => 
   -- H0
   V(0) <= S(0); W(0) <= S(4); C(0) <= inv_sqrt_2; D(0) <= inv_sqrt_2; 
   VV(0) <= T(0); WW(0) <= T(4); CC(0) <= inv_sqrt_2; DD(0) <= inv_sqrt_2; 
   V(1) <= S(1); W(1) <= S(5); C(1) <= inv_sqrt_2; D(1) <= inv_sqrt_2; 
   VV(1) <= T(1); WW(1) <= T(5); CC(1) <= inv_sqrt_2; DD(1) <= inv_sqrt_2; 
   V(2) <= S(2); W(2) <= S(6); C(2) <= inv_sqrt_2; D(2) <= inv_sqrt_2; 
   VV(2) <= T(2); WW(2) <= T(6); CC(2) <= inv_sqrt_2; DD(2) <= inv_sqrt_2; 
   V(3) <= S(3); W(3) <= S(7); C(3) <= inv_sqrt_2; D(3) <= inv_sqrt_2; 
   VV(3) <= T(3); WW(3) <= T(7); CC(3) <= inv_sqrt_2; DD(3) <= inv_sqrt_2; 
   V(4) <= S(0); W(4) <= S(4); C(4) <= inv_sqrt_2; D(4) <= minus_inv_sqrt_2; 
   VV(4) <= T(0); WW(4) <= T(4); CC(4) <= inv_sqrt_2; DD(4) <= minus_inv_sqrt_2; 
   V(5) <= S(1); W(5) <= S(5); C(5) <= inv_sqrt_2; D(5) <= minus_inv_sqrt_2; 
   VV(5) <= T(1); WW(5) <= T(5); CC(5) <= inv_sqrt_2; DD(5) <= minus_inv_sqrt_2; 
   V(6) <= S(2); W(6) <= S(6); C(6) <= inv_sqrt_2; D(6) <= minus_inv_sqrt_2; 
   VV(6) <= T(2); WW(6) <= T(6); CC(6) <= inv_sqrt_2; DD(6) <= minus_inv_sqrt_2; 
   V(7) <= S(3); W(7) <= S(7); C(7) <= inv_sqrt_2; D(7) <= minus_inv_sqrt_2; 
   VV(7) <= T(3); WW(7) <= T(7); CC(7) <= inv_sqrt_2; DD(7) <= minus_inv_sqrt_2;
   WHEN 2 => 
   -- CR_PI/2_10
   V(0) <= S(0); W(0) <= zero; C(0) <= one; D(0) <= zero; 
   VV(0) <= T(0); WW(0) <= zero; CC(0) <= one; DD(0) <= zero; 
   V(1) <= S(1); W(1) <= zero; C(1) <= one; D(1) <= zero; 
   VV(1) <= T(1); WW(1) <= zero; CC(1) <= one; DD(1) <= zero; 
   V(2) <= S(2); W(2) <= zero; C(2) <= one; D(2) <= zero; 
   VV(2) <= T(2); WW(2) <= zero; CC(2) <= one; DD(2) <= zero; 
   V(3) <= S(3); W(3) <= zero; C(3) <= one; D(3) <= zero; 
   VV(3) <= T(3); WW(3) <= zero; CC(3) <= one; DD(3) <= zero; 
   V(4) <= S(4); W(4) <= zero; C(4) <= one; D(4) <= zero; 
   VV(4) <= T(4); WW(4) <= zero; CC(4) <= one; DD(4) <= zero; 
   V(5) <= S(5); W(5) <= zero; C(5) <= one; D(5) <= zero; 
   VV(5) <= T(5); WW(5) <= zero; CC(5) <= one; DD(5) <= zero; 
   V(6) <= T(6); W(6) <= zero; C(6) <= minus_one; D(6) <= zero; 
   VV(6) <= S(6); WW(6) <= zero; CC(6) <= one; DD(6) <= zero; 
   V(7) <= T(7); W(7) <= zero; C(7) <= minus_one; D(7) <= zero; 
   VV(7) <= S(7); WW(7) <= zero; CC(7) <= one; DD(7) <= zero;
   WHEN 3 => 
   -- CR_PI/4_20
   V(0) <= S(0); W(0) <= zero; C(0) <= one; D(0) <= zero; 
   VV(0) <= T(0); WW(0) <= zero; CC(0) <= one; DD(0) <= zero; 
   V(1) <= S(1); W(1) <= zero; C(1) <= one; D(1) <= zero; 
   VV(1) <= T(1); WW(1) <= zero; CC(1) <= one; DD(1) <= zero; 
   V(2) <= S(2); W(2) <= zero; C(2) <= one; D(2) <= zero; 
   VV(2) <= T(2); WW(2) <= zero; CC(2) <= one; DD(2) <= zero; 
   V(3) <= S(3); W(3) <= zero; C(3) <= one; D(3) <= zero; 
   VV(3) <= T(3); WW(3) <= zero; CC(3) <= one; DD(3) <= zero; 
   V(4) <= S(4); W(4) <= zero; C(4) <= one; D(4) <= zero; 
   VV(4) <= T(4); WW(4) <= zero; CC(4) <= one; DD(4) <= zero; 
   V(5) <= S(5); W(5) <= T(5); C(5) <= inv_sqrt_2; D(5) <= minus_inv_sqrt_2; 
   VV(5) <= S(5); WW(5) <= T(5); CC(5) <= inv_sqrt_2; DD(5) <= inv_sqrt_2; 
   V(6) <= T(6); W(6) <= zero; C(6) <= minus_one; D(6) <= zero; 
   VV(6) <= S(6); WW(6) <= zero; CC(6) <= one; DD(6) <= zero; 
   V(7) <= S(7); W(7) <= T(7); C(7) <= inv_sqrt_2; D(7) <= minus_inv_sqrt_2; 
   VV(7) <= S(7); WW(7) <= T(7); CC(7) <= inv_sqrt_2; DD(7) <= inv_sqrt_2;
   WHEN 4 => 
   -- H1
   V(0) <= S(0); W(0) <= S(2); C(0) <= inv_sqrt_2; D(0) <= inv_sqrt_2; 
   VV(0) <= T(0); WW(0) <= T(2); CC(0) <= inv_sqrt_2; DD(0) <= inv_sqrt_2; 
   V(1) <= S(1); W(1) <= S(3); C(1) <= inv_sqrt_2; D(1) <= inv_sqrt_2; 
   VV(1) <= T(1); WW(1) <= T(3); CC(1) <= inv_sqrt_2; DD(1) <= inv_sqrt_2; 
   V(2) <= S(0); W(2) <= S(2); C(2) <= inv_sqrt_2; D(2) <= minus_inv_sqrt_2; 
   VV(2) <= T(0); WW(2) <= T(2); CC(2) <= inv_sqrt_2; DD(2) <= minus_inv_sqrt_2; 
   V(3) <= S(1); W(3) <= S(3); C(3) <= inv_sqrt_2; D(3) <= minus_inv_sqrt_2; 
   VV(3) <= T(1); WW(3) <= T(3); CC(3) <= inv_sqrt_2; DD(3) <= minus_inv_sqrt_2; 
   V(4) <= S(4); W(4) <= S(6); C(4) <= inv_sqrt_2; D(4) <= inv_sqrt_2; 
   VV(4) <= T(4); WW(4) <= T(6); CC(4) <= inv_sqrt_2; DD(4) <= inv_sqrt_2; 
   V(5) <= S(5); W(5) <= S(7); C(5) <= inv_sqrt_2; D(5) <= inv_sqrt_2; 
   VV(5) <= T(5); WW(5) <= T(7); CC(5) <= inv_sqrt_2; DD(5) <= inv_sqrt_2; 
   V(6) <= S(4); W(6) <= S(6); C(6) <= inv_sqrt_2; D(6) <= minus_inv_sqrt_2; 
   VV(6) <= T(4); WW(6) <= T(6); CC(6) <= inv_sqrt_2; DD(6) <= minus_inv_sqrt_2; 
   V(7) <= S(5); W(7) <= S(7); C(7) <= inv_sqrt_2; D(7) <= minus_inv_sqrt_2; 
   VV(7) <= T(5); WW(7) <= T(7); CC(7) <= inv_sqrt_2; DD(7) <= minus_inv_sqrt_2;
   WHEN 5 => 
   -- CR_PI/2_21
   V(0) <= S(0); W(0) <= zero; C(0) <= one; D(0) <= zero; 
   VV(0) <= T(0); WW(0) <= zero; CC(0) <= one; DD(0) <= zero; 
   V(1) <= S(1); W(1) <= zero; C(1) <= one; D(1) <= zero; 
   VV(1) <= T(1); WW(1) <= zero; CC(1) <= one; DD(1) <= zero; 
   V(2) <= S(2); W(2) <= zero; C(2) <= one; D(2) <= zero; 
   VV(2) <= T(2); WW(2) <= zero; CC(2) <= one; DD(2) <= zero; 
   V(3) <= T(3); W(3) <= zero; C(3) <= minus_one; D(3) <= zero; 
   VV(3) <= S(3); WW(3) <= zero; CC(3) <= one; DD(3) <= zero; 
   V(4) <= S(4); W(4) <= zero; C(4) <= one; D(4) <= zero; 
   VV(4) <= T(4); WW(4) <= zero; CC(4) <= one; DD(4) <= zero; 
   V(5) <= S(5); W(5) <= zero; C(5) <= one; D(5) <= zero; 
   VV(5) <= T(5); WW(5) <= zero; CC(5) <= one; DD(5) <= zero; 
   V(6) <= S(6); W(6) <= zero; C(6) <= one; D(6) <= zero; 
   VV(6) <= T(6); WW(6) <= zero; CC(6) <= one; DD(6) <= zero; 
   V(7) <= T(7); W(7) <= zero; C(7) <= minus_one; D(7) <= zero; 
   VV(7) <= S(7); WW(7) <= zero; CC(7) <= one; DD(7) <= zero;
   WHEN 6 => 
   -- H2
   V(0) <= S(0); W(0) <= S(1); C(0) <= inv_sqrt_2; D(0) <= inv_sqrt_2; 
   VV(0) <= T(0); WW(0) <= T(1); CC(0) <= inv_sqrt_2; DD(0) <= inv_sqrt_2; 
   V(1) <= S(0); W(1) <= S(1); C(1) <= inv_sqrt_2; D(1) <= minus_inv_sqrt_2; 
   VV(1) <= T(0); WW(1) <= T(1); CC(1) <= inv_sqrt_2; DD(1) <= minus_inv_sqrt_2; 
   V(2) <= S(2); W(2) <= S(3); C(2) <= inv_sqrt_2; D(2) <= inv_sqrt_2; 
   VV(2) <= T(2); WW(2) <= T(3); CC(2) <= inv_sqrt_2; DD(2) <= inv_sqrt_2; 
   V(3) <= S(2); W(3) <= S(3); C(3) <= inv_sqrt_2; D(3) <= minus_inv_sqrt_2; 
   VV(3) <= T(2); WW(3) <= T(3); CC(3) <= inv_sqrt_2; DD(3) <= minus_inv_sqrt_2; 
   V(4) <= S(4); W(4) <= S(5); C(4) <= inv_sqrt_2; D(4) <= inv_sqrt_2; 
   VV(4) <= T(4); WW(4) <= T(5); CC(4) <= inv_sqrt_2; DD(4) <= inv_sqrt_2; 
   V(5) <= S(4); W(5) <= S(5); C(5) <= inv_sqrt_2; D(5) <= minus_inv_sqrt_2; 
   VV(5) <= S(4); WW(5) <= S(5); CC(5) <= inv_sqrt_2; DD(5) <= minus_inv_sqrt_2; 
   V(6) <= S(6); W(6) <= S(7); C(6) <= inv_sqrt_2; D(6) <= inv_sqrt_2; 
   VV(6) <= T(6); WW(6) <= T(7); CC(6) <= inv_sqrt_2; DD(6) <= inv_sqrt_2; 
   V(7) <= S(6); W(7) <= S(7); C(7) <= inv_sqrt_2; D(7) <= minus_inv_sqrt_2; 
   VV(7) <= T(6); WW(7) <= T(7); CC(7) <= inv_sqrt_2; DD(7) <= minus_inv_sqrt_2;
   WHEN 7 => 
   -- NOP
   V(0) <= S(0); W(0) <= zero; C(0) <= one; D(0) <= zero; 
   VV(0) <= T(0); WW(0) <= zero; CC(0) <= one; DD(0) <= zero; 
   V(1) <= S(1); W(1) <= zero; C(1) <= one; D(1) <= zero; 
   VV(1) <= T(1); WW(1) <= zero; CC(1) <= one; DD(1) <= zero; 
   V(2) <= S(2); W(2) <= zero; C(2) <= one; D(2) <= zero; 
   VV(2) <= T(2); WW(2) <= zero; CC(2) <= one; DD(2) <= zero; 
   V(3) <= S(3); W(3) <= zero; C(3) <= one; D(3) <= zero; 
   VV(3) <= T(3); WW(3) <= zero; CC(3) <= one; DD(3) <= zero; 
   V(4) <= S(4); W(4) <= zero; C(4) <= one; D(4) <= zero; 
   VV(4) <= T(4); WW(4) <= zero; CC(4) <= one; DD(4) <= zero; 
   V(5) <= S(5); W(5) <= zero; C(5) <= one; D(5) <= zero; 
   VV(5) <= T(5); WW(5) <= zero; CC(5) <= one; DD(5) <= zero; 
   V(6) <= S(6); W(6) <= zero; C(6) <= one; D(6) <= zero; 
   VV(6) <= T(6); WW(6) <= zero; CC(6) <= one; DD(6) <= zero; 
   V(7) <= S(7); W(7) <= zero; C(7) <= one; D(7) <= zero; 
   VV(7) <= T(7); WW(7) <= zero; CC(7) <= one; DD(7) <= zero;
   END CASE;
   END PROCESS;
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
      clk, reset: IN STD_LOGIC;
      S_out, T_out: OUT Q_STATE(0 TO 7)
   );
   END COMPONENT;
   SIGNAL clk: STD_LOGIC := '0';
   SIGNAL reset: STD_LOGIC;
   SIGNAL S_out, T_out: Q_STATE(0 TO 7);
BEGIN
   dut: QFT_3 PORT MAP(clk, reset, S_out, T_out);
   clk <= NOT(clk) AFTER 50 ns;
   reset <= '1', '0' AFTER 100 ns;
END circuit;

