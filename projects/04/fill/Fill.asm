// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

    @8192   // 512*256/16 pixels
    D=A
    @buffer
    M=D     // Buffer size

(LOOP)
    @i
    M=0     // Loop variable

(INNER)
    @KBD
    D=M
    @WHITE
    D;JEQ   // Go to white if no key is pressed

(BLACK)
    @i
    D=M
    @SCREEN
    A=A+D   // Calculate address
    M=-1    // Set it to black
    @END
    0;JMP

(WHITE)
    @i
    D=M
    @SCREEN
    A=A+D
    M=0

(END)
    @i
    MD=M+1
    @buffer
    D=D-M
    @LOOP
    D;JEQ
    @INNER
    0;JMP

