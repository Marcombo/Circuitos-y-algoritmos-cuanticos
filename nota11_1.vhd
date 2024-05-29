library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
package qubits is
  constant t: natural := 10; -- t bits per fp number
  constant n: natural := 5; -- n qubits
  constant d: natural := 2**n; -- dimension_d space
  constant p: natural := 8; -- rom address size
  constant logn: natural := 3; -- 2**logn > n
  constant ws: natural := 2+2*logn+8*t; -- rom word size
  constant cs: natural := 2+2*logn; -- opcode size
  constant first: std_logic_vector(p-1 downto 0) := conv_std_logic_vector(0, p); -- natural = 00...0
  constant zero: std_logic_vector(t-1 downto 0) := conv_std_logic_vector(0, t); -- fp data = 00.00...0
  constant one: std_logic_vector(t-1 downto 0) := "01"&conv_std_logic_vector(0, t-2); -- fp data = 01.00...0 
  constant minus_one: std_logic_vector(t-1 downto 0) := "11"&conv_std_logic_vector(0, t-2); -- fp data = 11.00...0
  constant addr_zero:std_logic_vector(n-1 downto 0) := conv_std_logic_vector(0, n); -- address = 0
  type q_state is array (natural range <>) of std_logic_vector(t-1 downto 0);
end qubits;

library ieee; 
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
use work.qubits.all;
entity dual_port_ram is
port (
  data_in_A_re,data_in_A_im,data_in_B_re,data_in_B_im: in std_logic_vector(t-1 downto 0);
  clk, writeA, writeB: in std_logic := '0';
  address_A,address_B : in std_logic_vector(n-1 downto 0);
  data_out_A_re,data_out_A_im,data_out_B_re,data_out_B_im: out std_logic_vector(t-1 downto 0)
);
end dual_port_ram;

architecture behavior of dual_port_ram is
  type memory is array (0 to d-1) of std_logic_vector(t-1 downto 0);
  signal X_re, X_im: memory;
  signal EN_A, EN_B: std_logic_vector(0 to d-1);
begin
  decoder_A: process(address_A, writeA)
  begin
    for i in 0 to d-1 loop
      if i = conv_integer(address_A) then EN_A(i) <= writeA;
      else EN_A(i) <= '0';
      end if;
    end loop;
  end process;
  decoder_B: process(address_B, writeB)
  begin
    for i in 0 to d-1 loop
      if i = conv_integer(address_B) then EN_B(i) <= writeB;
      else EN_B(i) <= '0';
      end if;
    end loop;
  end process;
 register_bank: process(clk)
 begin
     if clk'event and clk = '1' then
       for i in 0 to d-1 loop
         if EN_A(i) = '1' then X_re(i) <= data_in_A_re; X_im(i) <= data_in_A_im; end if;
         if EN_B(i) = '1' then X_re(i) <= data_in_B_re; X_im(i) <= data_in_B_im; end if;
       end loop;
     end if;
  end process;
  multiplexer: process(address_A,address_B, X_re, X_im)
  begin
     for i in 0 to d-1 loop
        if i = conv_integer(address_A) then  data_out_A_re <= X_re(i);data_out_A_im <= X_im(i); end if;
        if i = conv_integer(address_B) then  data_out_B_re <= X_re(i);data_out_B_im <= X_im(i); end if;
     end loop;
   end process;  
end behavior;

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
use work.qubits.all;
entity fp_mul is
   port(
      a, b: in std_logic_vector(t-1 downto 0);
      c: out std_logic_vector(t-1 downto 0)
      );
end fp_mul;
architecture behavior of fp_mul is
   signal long_a, long_b: std_logic_vector(2*t-1 downto 0); 
   signal long_c: std_logic_vector(4*t-1 downto 0);   
begin
   long_a(2*t-1 downto t)<= (others => a(t-1));
   long_a(t-1 downto 0)<= a;
   long_b(2*t-1 downto t)<= (others => b(t-1));
   long_b(t-1 downto 0)<= b; 
   long_c <=  long_a*long_b;
   c <= long_c(2*t-3 downto t-2);
end behavior;

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
use work.qubits.all;
entity ar_unit is
port (
  inA_re,inA_im,inB_re,inB_im: in std_logic_vector(t-1 downto 0);
  output01: in std_logic;
  outA_re,outA_im,outB_re,outB_im: out std_logic_vector(t-1 downto 0);
  a_re,a_im,b_re,b_im, c_re,c_im,d_re,d_im: in std_logic_vector(t-1 downto 0)  
);
end ar_unit;

architecture circuit of ar_unit is
  component fp_mul is
  port (
  a, b: in std_logic_vector(t-1 downto 0);
  c: out std_logic_vector(t-1 downto 0)
  );
  end component;
  signal 
  areAre,aimAim,breBre,bimBim,aimAre,areAim,bimBre,breBim,creAre,cimAim,dreBre,dimBim,cimAre,creAim,dimBre,dreBim: std_logic_vector(t-1 downto 0);
begin
  mul1: fp_mul port map(a_re, inA_re, areAre);
  mul2: fp_mul port map(a_im, inA_im, aimAim);
  mul3: fp_mul port map(b_re, inB_re, breBre);
  mul4: fp_mul port map(b_im, inB_im, bimBim);
  mul5: fp_mul port map(a_im, inA_re, aimAre);
  mul6: fp_mul port map(a_re, inA_im, areAim);
  mul7: fp_mul port map(b_im, inB_re, bimBre);
  mul8: fp_mul port map(b_re, inB_im, breBim);
  mul9: fp_mul port map(c_re, inA_re, creAre);
  mul10: fp_mul port map(c_im, inA_im, cimAim);
  mul11: fp_mul port map(d_re, inB_re, dreBre);
  mul12: fp_mul port map(d_im, inB_im, dimBim);
  mul13: fp_mul port map(c_im, inA_re, cimAre);
  mul14: fp_mul port map(c_re, inA_im, creAim);
  mul15: fp_mul port map(d_im, inB_re, dimBre);
  mul16: fp_mul port map(d_re, inB_im, dreBim);
  process(output01,areAre,aimAim,breBre,bimBim,aimAre,areAim,bimBre,breBim,creAre,cimAim,dreBre,dimBim,cimAre,creAim,dimBre,dreBim )
  begin
    if output01 = '1' then
    outA_re <= zero; outA_im <= zero; outB_re <= one; outB_im <= zero;
  else
    outA_re <= areAre - aimAim + breBre - bimBim;
    outA_im <= aimAre + areAim + bimBre + breBim;
    outB_re <= creAre - cimAim + dreBre - dimBim;
    outB_im <= cimAre + creAim + dimBre + dreBim;
  end if;
  end process;
end circuit;

library ieee; 
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
use work.qubits.all;
entity program_memory is
port (
  address_M: in std_logic_vector(p-1 downto 0);
  instruction: out std_logic_vector(ws-1 downto 0)
);
end program_memory;

architecture behavior of program_memory is
  type format is record
    op: std_logic_vector(1 downto 0);
    l: std_logic_vector(logn-1 downto 0);
    k: std_logic_vector(logn-1 downto 0);
    ar: std_logic_vector(t-1 downto 0);
    ai: std_logic_vector(t-1 downto 0);
    br: std_logic_vector(t-1 downto 0);
    bi: std_logic_vector(t-1 downto 0);
    cr: std_logic_vector(t-1 downto 0);
    ci: std_logic_vector(t-1 downto 0);
    dr: std_logic_vector(t-1 downto 0);
    di: std_logic_vector(t-1 downto 0);
  end record;
  type memory is array (0 to 2**p-1) of format;
  signal contents: memory := (  
  ("00", "000", "000","00"&x"00","00"&x"00","00"&x"00","00"&x"00", "00"&x"00","00"&x"00","00"&x"00","00"&x"00"), -- init
  ("01", "000", "001","00"&x"00","00"&x"00","01"&x"00","00"&x"00", "01"&x"00","00"&x"00","00"&x"00","00"&x"00"), -- X(1)
  ("01", "000", "011","00"&x"00","00"&x"00","01"&x"00","00"&x"00", "01"&x"00","00"&x"00","00"&x"00","00"&x"00"), -- X(3)
  ("01", "000", "000","00"&x"b5","00"&x"00","00"&x"b5","00"&x"00", "00"&x"b5","00"&x"00","11"&x"4b","00"&x"00"), -- H(0)
  ("10", "001", "000","01"&x"00","00"&x"00","00"&x"00","00"&x"00", "00"&x"00","00"&x"00","00"&x"00","01"&x"00"), -- CRphi(1,0, pi/2)
  ("10", "010", "000","01"&x"00","00"&x"00","00"&x"00","00"&x"00", "00"&x"00","00"&x"00","00"&x"b5","00"&x"b5"), -- CRphi(2,0, pi/4)
  ("10", "011", "000","01"&x"00","00"&x"00","00"&x"00","00"&x"00", "00"&x"00","00"&x"00","00"&x"ec","00"&x"62"), -- CRphi(3,0, pi/8)
  ("01", "000", "001","00"&x"b5","00"&x"00","00"&x"b5","00"&x"00", "00"&x"b5","00"&x"00","11"&x"4b","00"&x"00"), -- H(1)
  ("10", "010", "001","01"&x"00","00"&x"00","00"&x"00","00"&x"00", "00"&x"00","00"&x"00","00"&x"00","01"&x"00"), -- CRphi(2,1, pi/2)
  ("10", "011", "001","01"&x"00","00"&x"00","00"&x"00","00"&x"00", "00"&x"00","00"&x"00","00"&x"b5","00"&x"b5"), -- CRphi(3,1, pi/4)
  ("01", "000", "010","00"&x"b5","00"&x"00","00"&x"b5","00"&x"00", "00"&x"b5","00"&x"00","11"&x"4b","00"&x"00"), -- H(2)
  ("10", "011", "010","01"&x"00","00"&x"00","00"&x"00","00"&x"00", "00"&x"00","00"&x"00","00"&x"00","01"&x"00"), -- CRphi(3,2, pi/2)
  ("01", "000", "011","00"&x"b5","00"&x"00","00"&x"b5","00"&x"00", "00"&x"b5","00"&x"00","11"&x"4b","00"&x"00"), -- H(3)
   others => ("11", "000", "000","00"&x"00","00"&x"00","00"&x"00","00"&x"00", "00"&x"00","00"&x"00","00"&x"00","00"&x"00") -- end
  );
begin
   rom: process(address_M)
     variable i: natural;
     variable form_instruction: format;
   begin
     i := conv_integer(address_M);
     form_instruction := contents(i); 
     instruction <= form_instruction.op & form_instruction.l &  form_instruction.k & form_instruction.ar & form_instruction.ai & form_instruction.br & 
     form_instruction.bi & form_instruction.cr & form_instruction.ci & form_instruction.dr & form_instruction.di; 
   end process;
end behavior;	

library ieee; 
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
use work.qubits.all;
entity processor is
port (
  clk, reset:in std_logic;
  opcode: in std_logic_vector(cs-1 downto 0);
  writeA, writeB,output01: out std_logic;
  address_A,address_B : out std_logic_vector(n-1 downto 0);
  address_M: inout std_logic_vector(p-1 downto 0)
);
end processor;

architecture behavior of processor is
begin
  processor: process
   variable s, k, l, m, q: integer;  
   variable addr: std_logic_vector(n-1 downto 0);
  begin
    address_M <= first;
    wait until clk'event and clk = '1';
    loop
      case opcode(cs-1 downto cs-2) is
        when "00" => 
          output01 <= '1';
          address_A <= addr_zero;
          address_B <= addr_zero;
          writeA <= '0';
          writeB <= '1';
          wait until clk'event and clk = '1';
          for i in 1 to d-1 loop
              address_A <= conv_std_logic_vector(i, n);
              writeA <= '1';
              writeB <= '0';
              wait until clk'event and clk = '1';
          end loop;   
          writeA <= '0';
          writeB <= '0';
          output01 <= '0';
          address_M <= address_M + 1;
        when "01" =>
          k := conv_integer(opcode(logn-1 downto 0));
          m := 2**(n-k-1);
          q := 2**k;
          for j in 0 to q-1 loop
            s := 2*m*j;
            for i in s to s+m-1 loop
              address_A <= conv_std_logic_vector(i, n);
              address_B <= conv_std_logic_vector(i+m, n);
              writeA <= '1';
              writeB <= '1';
              wait until clk'event and clk = '1';  
            end loop;
           end loop;
           writeA <= '0';
           writeB <= '0';
          address_M <= address_M + 1;
        when "11" =>
          writeA <= '0';
          writeB <= '0';
          output01 <= '0';
        when "10" =>
          k := conv_integer(opcode(logn-1 downto 0));
          l := conv_integer(opcode(cs-3 downto logn));
          m := 2**(n-k-1);
          q := 2**k;
          for j in 0 to q-1 loop
            s := 2*m*j;
            for i in s to s+m-1 loop
              addr := conv_std_logic_vector(i, n);
              address_A <= addr;
              address_B <= conv_std_logic_vector(i+m, n);
              if addr(n-1-l) = '1' then
                writeA <= '1';
                writeB <= '1';
              else
                writeA <= '0';
                writeB <= '0';
              end if;               
              wait until clk'event and clk = '1';  
            end loop;
           end loop;
           writeA <= '0';
           writeB <= '0';
          address_M <= address_M + 1;
        when others =>           
          writeA <= '0';
          writeB <= '0';
          output01 <= '0';
         end case;
       wait until clk'event and clk = '1';
      end loop;
    end process;
end behavior;

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
use work.qubits.all;

entity emulator is
port (clk, reset: in std_logic);
end emulator;
architecture circuit of emulator is
component dual_port_ram is
port (
  data_in_A_re,data_in_A_im,data_in_B_re,data_in_B_im: in std_logic_vector(t-1 downto 0);
  clk, writeA, writeB: in std_logic := '0';
  address_A,address_B : in std_logic_vector(n-1 downto 0);
  data_out_A_re,data_out_A_im,data_out_B_re,data_out_B_im: out std_logic_vector(t-1 downto 0)
  );
end component;
component ar_unit is
port (
  inA_re,inA_im,inB_re,inB_im: in std_logic_vector(t-1 downto 0);
  output01: in std_logic;
  outA_re,outA_im,outB_re,outB_im: out std_logic_vector(t-1 downto 0);
  a_re,a_im,b_re,b_im, c_re,c_im,d_re,d_im: in std_logic_vector(t-1 downto 0)  
);
end component;
component processor is
port (
  clk, reset:in std_logic;
  opcode: in std_logic_vector(cs-1 downto 0);
  writeA, writeB,output01: out std_logic;
  address_A,address_B : out std_logic_vector(n-1 downto 0);
  address_M: inout std_logic_vector(p-1 downto 0)
);
end component;
component program_memory is
port (
  address_M: in std_logic_vector(p-1 downto 0);
  instruction: out std_logic_vector(ws-1 downto 0)
);
end component;
signal data_in_A_re,data_in_A_im,data_in_B_re,data_in_B_im: std_logic_vector(t-1 downto 0);
signal writeA, writeB, output01: std_logic;
signal address_A,address_B : std_logic_vector(n-1 downto 0);
signal inA_re,inA_im,inB_re,inB_im: std_logic_vector(t-1 downto 0);
signal instruction: std_logic_vector(ws-1 downto 0);
signal address_M: std_logic_vector(p-1 downto 0);
begin
dpram: dual_port_ram port map (
  data_in_A_re,data_in_A_im,data_in_B_re,data_in_B_im, clk, writeA, writeB,
  address_A,address_B,inA_re,inA_im,inB_re,inB_im);
arithmetic_unit: ar_unit port map (
  inA_re,inA_im,inB_re,inB_im,output01,data_in_A_re,data_in_A_im,data_in_B_re,data_in_B_im,
  instruction(ws-3-2*logn downto ws-12-2*logn),instruction(ws-13-2*logn downto ws-22-2*logn),
  instruction(ws-23-2*logn downto ws-32-2*logn),instruction(ws-33-2*logn downto ws-42-2*logn),
  instruction(ws-43-2*logn downto ws-52-2*logn),instruction(ws-53-2*logn downto ws-62-2*logn),
  instruction(ws-63-2*logn downto ws-72-2*logn),instruction(ws-73-2*logn downto 0)); 
control_unit: processor port map (
  clk, reset, instruction(ws-1 downto ws-2-2*logn),writeA, writeB, output01, address_A, address_B,address_M);
rom: program_memory port map(address_M, instruction);
end circuit;


library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
use work.qubits.all;

entity fourier is end fourier;

architecture test of fourier is
component emulator is
port (clk, reset: in std_logic);
end component;
signal clk: std_logic := '0';
signal reset: std_logic;
begin
dut: emulator port map (clk, reset);
clk <= not(clk) after 10 ns; 
reset <= '0';
end test;




