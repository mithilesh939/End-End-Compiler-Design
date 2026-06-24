# Jack Compiler — DA2304 Assignment 3

## Pipeline
This project contains:

- A Jack Compiler written in Python
- Tokenizer, Symbol Table, VM Writer, and Compilation Engine modules
- A Jack implementation of 2D Convolution (`Conv.jack`)
- A driver program (`Main.jack`) for testing convolution

The compiler converts `.jack` files into:
- XML parse/token files
- VM code files

## Compiler Files

- `JackCompiler.py` → Main compiler driver
- `JackTokenizer.py` → Tokenizes Jack source code
- `CompilationEngine.py` → Parses Jack grammar and generates VM code
- `SymbolTable.py` → Manages variable scopes and symbol information
- `VMWriter.py` → Writes VM commands


## Jack Programs

- `Conv.jack` → Implements 2D convolution logic
- `Main.jack` → Creates test matrices and runs convolution

## Note About Generated Files

The compiler currently generates some intermediate `.xml` and `.vm` files inside the `jack/` directory in addition to the `out/` directory due to path-handling differences across modules.

However, all required final generated artefacts are successfully produced and included inside the `out/` folder as required by the assignment specification.

# How to Run

## Compile Jack Files

Open terminal inside the project folder and run:

```bash
python JackCompiler.py .
python JackCompiler.py ../jack