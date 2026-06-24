import os

class CodeWriter:
    def __init__(self, outfile):
        self.f = open(outfile, "w")
        self.label_n = 0
        self.fname = ""
        self.cur_func = ""

    def set_file(self, path):
        self.fname = os.path.splitext(os.path.basename(path))[0]
        self.cur_func = "" 
    def w(self, line):
        self.f.write(line + "\n")

    
    def push_d(self):
        self.w("@SP")
        self.w("A=M")
        self.w("M=D")
        self.w("@SP")
        self.w("M=M+1")

    def pop_to_d(self):
        self.w("@SP")
        self.w("AM=M-1")
        self.w("D=M")

    
    def write_arith(self, cmd):
        if cmd == "add":
            self.pop_to_d()
            self.w("A=A-1")
            self.w("M=D+M")

        elif cmd == "sub":
            self.pop_to_d()
            self.w("A=A-1")
            self.w("M=M-D")

        elif cmd == "neg":
            self.w("@SP")
            self.w("A=M-1")
            self.w("M=-M")

        elif cmd == "and":
            self.pop_to_d()
            self.w("A=A-1")
            self.w("M=D&M")

        elif cmd == "or":
            self.pop_to_d()
            self.w("A=A-1")
            self.w("M=D|M")

        elif cmd == "not":
            self.w("@SP")
            self.w("A=M-1")
            self.w("M=!M")

        elif cmd in ["eq", "gt", "lt"]:
            t = f"TRUE{self.label_n}"
            e = f"END{self.label_n}"
            self.label_n += 1

            self.pop_to_d()
            self.w("A=A-1")
            self.w("D=M-D")
            self.w(f"@{t}")

            if cmd == "eq": self.w("D;JEQ")
            if cmd == "gt": self.w("D;JGT")
            if cmd == "lt": self.w("D;JLT")

            self.w("@SP")
            self.w("A=M-1")
            self.w("M=0")
            self.w(f"@{e}")
            self.w("0;JMP")

            self.w(f"({t})")
            self.w("@SP")
            self.w("A=M-1")
            self.w("M=-1")
            self.w(f"({e})")

    
    def write_push_pop(self, ctype, seg, idx):
        seg_map = {"local":"LCL","argument":"ARG","this":"THIS","that":"THAT"}

        if ctype == "C_PUSH":
            if seg == "constant":
                self.w(f"@{idx}")
                self.w("D=A")

            elif seg in seg_map:
                base = seg_map[seg]
                self.w(f"@{base}")
                self.w("D=M")
                self.w(f"@{idx}")
                self.w("A=D+A")
                self.w("D=M")

            elif seg == "temp":
                self.w(f"@{5 + idx}")
                self.w("D=M")

            elif seg == "pointer":
                reg = "THIS" if idx == 0 else "THAT"
                self.w(f"@{reg}")
                self.w("D=M")

            elif seg == "static":
                self.w(f"@{self.fname}.{idx}")
                self.w("D=M")

            self.push_d()

        elif ctype == "C_POP":
            if seg in seg_map:
                base = seg_map[seg]
                self.w(f"@{base}")
                self.w("D=M")
                self.w(f"@{idx}")
                self.w("D=D+A")
                self.w("@R13")
                self.w("M=D")
                self.pop_to_d()
                self.w("@R13")
                self.w("A=M")
                self.w("M=D")

            elif seg == "temp":
                self.pop_to_d()
                self.w(f"@{5 + idx}")
                self.w("M=D")

            elif seg == "pointer":
                reg = "THIS" if idx == 0 else "THAT"
                self.pop_to_d()
                self.w(f"@{reg}")
                self.w("M=D")

            elif seg == "static":
                self.pop_to_d()
                self.w(f"@{self.fname}.{idx}")
                self.w("M=D")

    
    def write_label(self, label):
        self.w(f"({self.cur_func}${label})")

    def write_goto(self, label):
        self.w(f"@{self.cur_func}${label}")
        self.w("0;JMP")

    def write_if(self, label):
        self.pop_to_d()
        self.w(f"@{self.cur_func}${label}")
        self.w("D;JNE")

    # ---------------- FUNCTIONS ----------------
    def write_function(self, name, n_locals):
        self.cur_func = name
        self.w(f"({name})")

        for _ in range(n_locals):
            self.w("@0")
            self.w("D=A")
            self.push_d()

    
    def write_call(self, name, n_args):
        ret = f"{name}$ret{self.label_n}"
        self.label_n += 1

        
        self.w(f"@{ret}")
        self.w("D=A")
        self.push_d()

        
        for seg in ["LCL", "ARG", "THIS", "THAT"]:
            self.w(f"@{seg}")
            self.w("D=M")
            self.push_d()

        
        self.w("@SP")
        self.w("D=M")
        self.w("@5")
        self.w("D=D-A")
        self.w(f"@{n_args}")
        self.w("D=D-A")
        self.w("@ARG")
        self.w("M=D")

        # LCL = SP
        self.w("@SP")
        self.w("D=M")
        self.w("@LCL")
        self.w("M=D")

        # goto function
        self.w(f"@{name}")
        self.w("0;JMP")

        # return label
        self.w(f"({ret})")

   
    def write_return(self):
        # FRAME = LCL
        self.w("@LCL")
        self.w("D=M")
        self.w("@R13")
        self.w("M=D")

        
        self.w("@5")
        self.w("A=D-A")
        self.w("D=M")
        self.w("@R14")
        self.w("M=D")

        # *ARG = pop()
        self.pop_to_d()
        self.w("@ARG")
        self.w("A=M")
        self.w("M=D")

        
        self.w("@ARG")
        self.w("D=M+1")
        self.w("@SP")
        self.w("M=D")

        
        for seg in ["THAT", "THIS", "ARG", "LCL"]:
            self.w("@R13")
            self.w("AM=M-1")
            self.w("D=M")
            self.w(f"@{seg}")
            self.w("M=D")

       
        self.w("@R14")
        self.w("A=M")
        self.w("0;JMP")

    def close(self):
        self.f.close()