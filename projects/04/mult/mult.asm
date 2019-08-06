// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

    @R1
    D=M     // Save value of R1
    @i
    M=D     // Save value of R1 to i
    @R2
    M=0     // Initialize the result to 0

(LOOP)
    @i  
    D=M     // Load i
    @END
    D;JEQ   // If i == 0, end loop

    @R0
    D=M
    @R2
    M=M+D   // Add R0 to R2

    @i
    M=M-1   // Decrement i

    @LOOP
    0;JMP

(END)
    @END
    0;JMP