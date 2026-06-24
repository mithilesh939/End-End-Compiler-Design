class Parser:
    def __init__(self, fname):
        with open(fname) as f:
            lines = f.readlines()

        self.cmds = []
        self.pos = -1
        self.cmd = ""

        for line in lines:
            line = line.split("//")[0].strip()
            if line:
                self.cmds.append(line)

    def has_more(self):
        return self.pos + 1 < len(self.cmds)

    def advance(self):
        self.pos += 1
        self.cmd = self.cmds[self.pos]

    def cmd_type(self):
        w = self.cmd.split()[0]
        if w == "push":        return "C_PUSH"
        if w == "pop":         return "C_POP"
        if w == "label":       return "C_LABEL"
        if w == "goto":        return "C_GOTO"
        if w == "if-goto":     return "C_IF"
        if w == "function":    return "C_FUNCTION"
        if w == "call":        return "C_CALL"
        if w == "return":      return "C_RETURN"
        return "C_ARITHMETIC"

    def arg1(self):
        t = self.cmd_type()
        if t == "C_ARITHMETIC":
            return self.cmd.split()[0]
        if t != "C_RETURN":
            return self.cmd.split()[1]
        return None

    def arg2(self):
        t = self.cmd_type()
        if t in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            return int(self.cmd.split()[2])
        return None