
import sys
import os


sys.path.insert(0, os.path.dirname(__file__))

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


def compile_file(path: str):
    print(f'\n--- Compiling {path} ---')

    # create out folder
    project_root = os.path.dirname(
        os.path.dirname(
           os.path.abspath(path)
        )
    )
    out_dir = os.path.join(project_root, "out")

    os.makedirs(out_dir, exist_ok=True)

    tokenizer = JackTokenizer(path)
    tokens = tokenizer.tokenize()

    # get filename without extension
    base = os.path.splitext(os.path.basename(path))[0]

    # output base path
    out_path = os.path.join(out_dir, base)

    engine = CompilationEngine(tokens, out_path)
    engine.compile_class()


def main():
    if len(sys.argv) < 2:
        print("Usage: python JackCompiler.py <file.jack | directory>")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isdir(target):
        jack_files = [
            os.path.join(target, f)
            for f in os.listdir(target)
            if f.endswith('.jack')
        ]
        if not jack_files:
            print(f"No .jack files found in {target}")
            sys.exit(1)
        for f in sorted(jack_files):
            compile_file(f)
    elif os.path.isfile(target):
        compile_file(target)
    else:
        print(f"Path not found: {target}")
        sys.exit(1)

    print('\nCompilation complete.')


if __name__ == '__main__':
    main()
