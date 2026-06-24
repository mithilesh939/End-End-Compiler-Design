import sys
import os
from parser import Parser
from codewriter import CodeWriter


def translate(vm_file, writer):
    writer.set_file(vm_file)
    p = Parser(vm_file)

    while p.has_more():
        p.advance()
        t = p.cmd_type()

        if t == "C_ARITHMETIC":
            writer.write_arith(p.arg1())

        elif t in ["C_PUSH", "C_POP"]:
            writer.write_push_pop(t, p.arg1(), p.arg2())

        elif t == "C_LABEL":
            writer.write_label(p.arg1())

        elif t == "C_GOTO":
            writer.write_goto(p.arg1())

        elif t == "C_IF":
            writer.write_if(p.arg1())

        elif t == "C_FUNCTION":
            writer.write_function(p.arg1(), p.arg2())

        elif t == "C_CALL":
            writer.write_call(p.arg1(), p.arg2())

        elif t == "C_RETURN":
            writer.write_return()


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <file.vm or folder>")
        return

    path = sys.argv[1]

    
    if os.path.isdir(path):
        vm_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".vm")]
        out = os.path.join(path, os.path.basename(path.rstrip("/\\")) + ".asm")
    elif path.endswith(".vm"):
        vm_files = [path]
        out = path.replace(".vm", ".asm")
    else:
        print("Give a .vm file or a folder")
        return

    writer = CodeWriter(out)

    
    writer.w("@256")
    writer.w("D=A")
    writer.w("@SP")
    writer.w("M=D")

    if any(x in path for x in ["FunctionCalls", "ProgramFlow", "ch08", "08"]):
        writer.write_call("Sys.init", 0)
    is_project8 = ("ch08" in path or "FunctionCalls" in path or "ProgramFlow" in path)

    if is_project8:
        writer.write_call("Sys.init", 0)

    
    for vm in vm_files:
        translate(vm, writer)

    #
    writer.w("@END")
    writer.w("0;JMP")

    writer.w("(END)")
    writer.w("@END")
    writer.w("0;JMP")

    writer.close()

    print(f"Done! Output: {out}")


if __name__ == "__main__":
    main()
