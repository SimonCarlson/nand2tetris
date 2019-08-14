class Parser():
    parsed_lines = []

    def __init__(self, file):
        with open(file) as f:
            for line in f:
                l = self.parse(line)
                if len(l) > 0:
                    self.parsed_lines.append(l)

    def parse(self, line):
        try:
            index = line.index("//")
            line = line[:index]
        except ValueError:
            print("No comment")
    
        line = line.strip()
        return line

    def lines(self):
        for i in self.parsed_lines:
            yield i

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
        a = line.split("=")[0]  # split("=") -> [M, D+1; JGT]
        return a.strip()

    def getComp(self, line):
        a = line.split("=")[1]
        b = a.split(";")[0]
        return b.strip()

    def getJump(self, line):
        a = line.split(";")
        try:
            a = a[1]
        except IndexError:
            a = ""
        return a.strip()


if __name__ == "__main__":
    file = "add/Add.asm"    # @FIXME: Accept path as argument
    parser = Parser(file)
    for l in parser.lines():
        c = parser.getCommandType(l)
        if c is 0:
            print(parser.getDest(l), parser.getComp(l), parser.getJump(l))
            
            