import argparse
import os

class Parser():
    parsed_lines = []
    address = 0

    def __init__(self, file):
        with open(file) as f:
            for line in f:
                l = self.parse(line)
                if len(l) > 0:
                    self.parsed_lines.append(l)

    def parse(self, line):
        index = line.find("//")
        if index > -1:
            line = line[:index]
        
        line = line.strip()
        return line

    def lines(self):
        for i in self.parsed_lines:
            self.address += 1
            yield (i, self.address)


    def getCommandType(self, line):
        i = line.find("(")
        if i is -1: 
            j = line.find("@")
            if j is -1:
                return 0    # C-command
            return 1        # A-command
        return 2            # L-command (label)

    def getSymbol(self, line):
        i = line.find("(")
        if i > -1:          # Loop label, return (symbol)
            j = line.find(")")
            return line[i + 1:j]

        i = line.find("@")
        return line[i + 1:] # Return @symbol

    def getDest(self, line):    # M=D+1; JGT
        a = line.split("=")  # split("=") -> [M, D+1; JGT]
        if len(a) > 1:
            return a[0].strip()
        else:   # If dest is null the string does not contain = thus does not split
            return ""

    def getComp(self, line):
        #a = line.split("=")[1]
        a = line.split("=")
        if len(a) is 1:
            b = a[0].split(";")[0]
        else:
            b = a[1].split(";")[0]
        return b.strip()

    def getJump(self, line):
        a = line.split(";")
        try:
            a = a[1]
        except IndexError:
            a = ""
        return a.strip()

def destCode(dest):
    table = {"":"000", "M":"001", "D":"010", "MD":"011", "A":"100", "AM":"101", "AD":"110", "AMD":"111"}
    return table[dest]  # @FIXME: KeyError? Also, null?

def compCode(comp):
    a = "0"
    notaTable = {"0":"101010", "1":"111111", "-1":"111010", "D":"001100", "A":"110000", "!D":"001101", "!A":"110001", 
    "-D":"001111", "-A":"110011", "D+1":"011111", "A+1":"110111", "D-1":"001110", "A-1":"110010", "D+A":"000010",
    "D-A":"010011", "A-D":"000111", "D&A":"000000", "D|A":"010101"}
    aTable = {"M":"110000", "!M":"110001", "-M":"110011", "M+1":"110111", "M-1":"110010", "D+M":"000010", "D-M":"010011",
    "M-D":"000111", "D&M":"000000", "D|M":"010101"}

    try:
        c = notaTable[comp]
        return a + c
    except KeyError:
        c = aTable[comp]
        a = "1"
        return a + c

def jumpCode(jump):
    table = {"":"000", "JGT":"001", "JEQ":"010", "JGE":"011", "JLT":"100", "JNE":"101", "JLE":"110", "JMP":"111"}
    return table[jump]  # @FIXME KeyError? Also, null?

def init_symbol_table():
    symbols = {}
    symbols["R0"] = 0
    symbols["R1"] = 1
    symbols["R2"] = 2
    symbols["R3"] = 3
    symbols["R4"] = 4
    symbols["R5"] = 5
    symbols["R6"] = 6
    symbols["R7"] = 7
    symbols["R8"] = 8
    symbols["R9"] = 9
    symbols["R10"] = 10
    symbols["R11"] = 11
    symbols["R12"] = 12
    symbols["R13"] = 13
    symbols["R14"] = 14
    symbols["R15"] = 15
    symbols["SCREEN"] = 16384
    symbols["KBD"] = 24576
    symbols["SP"] = 0
    symbols["LCL"] = 1
    symbols["ARG"] = 2
    symbols["THIS"] = 3
    symbols["THAT"] = 4

    return symbols

def dec_to_binary(i):
    i = int(i) 
    return bin(i)[2:]   # Cut off 0b

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("path", metavar="path", type=str, help="Path to Hack assembly code")
    args = args.parse_args()
    path = args.path
    abspath = os.path.abspath(path)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname)

    parser = Parser(abspath)
    symbols = init_symbol_table()
    free_address = 16       # 0-15 are reserved

    # First pass: only look for labels and symbols
    for (l, address) in parser.lines():
        t = parser.getCommandType(l)
        
        if t is 2:    # L-command (label)
            s = parser.getSymbol(l)
            try:
                v = symbols[s]
                continue
            except KeyError: # Add the address for the instruction following the label
                symbols[s] = address - 1 - len(symbols) + 23 # Dont count labels for addresses, account for pre-initialized symbols


    outname = os.path.basename(abspath).split(".")[0]
    f = open(outname + ".hack", "w")
    # Second pass, translate and output commands
    for (l, address) in parser.lines():
        t = parser.getCommandType(l)
        instruction = ""

        if t is 0:      # C-command
            d = parser.getDest(l)
            c = parser.getComp(l)
            j = parser.getJump(l)

            dc = destCode(d)
            cc = compCode(c)
            jc = jumpCode(j)
            
            instruction = "111" + cc + dc + jc
        elif t is 1:    # A-command
            s = parser.getSymbol(l)
            v = ""
            try:    
                int(s)
                v = s   # It was a literal, use it
            except ValueError:  # It is a symbol
                try:
                    v = symbols[s]  # Value was found in symbol table
                except KeyError:    # It is not in the table
                    symbols[s] = free_address
                    v = free_address
                    free_address += 1   # Increment for next add
            
            vb = dec_to_binary(v)
            instruction = vb.zfill(16)  # Fill with leading zeros
        elif t is 2:    # Label
            # Skip, since we already added labels and they will be translated
            # as A-commands
            continue

        f.write(instruction + "\n")
        instruction = ""

    f.close()

            