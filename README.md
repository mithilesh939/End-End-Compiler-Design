# End-to-End Compiler Design

This repository contains the implementation and reports for three Compiler Design assignments completed as part of the DA2304 Compiler Design course. The project covers hardware construction, virtual machine translation, and the development of a Jack language compiler for the Hack computer platform.

## Repository Structure

```
.
├── DA2304_Assignment1_da24b048/
├── da2304_assignment2_da24b048/
├── DA2304_Assignment3_da24b048/
└── README.md
```

---

# Assignment 1 – Memory Architecture and Hardware Design

## Overview

This assignment focuses on the design and implementation of memory components in the Hack computer architecture using Hardware Description Language (HDL).

## Implemented Components

* Bit
* Register
* RAM8
* RAM64
* RAM512
* RAM4K
* RAM8K
* RAM16K

## Concepts Covered

* Data Flip-Flops (DFF)
* Registers and Load Signals
* Multiplexers and Demultiplexers
* Memory Addressing
* RAM Hierarchy Construction
* Memory Organization and Scalability

## Files

* `Bit.hdl`
* `Register.hdl`
* `RAM8.hdl`
* `RAM64.hdl`
* `RAM512.hdl`
* `RAM4K.hdl`
* `RAM8K.hdl`
* `RAM16K.hdl`

## Learning Outcomes

* Understanding sequential logic circuits
* Building hierarchical memory systems
* Implementing address selection logic
* Designing scalable memory architectures

---

# Assignment 2 – VM Translator

## Overview

This assignment implements a Virtual Machine (VM) Translator that converts Hack VM commands into Hack Assembly language.

The translator processes VM programs and generates equivalent assembly instructions that can be executed on the Hack computer.

## Features

### Arithmetic Commands

* add
* sub
* neg
* and
* or
* not
* eq
* gt
* lt

### Memory Access Commands

* push
* pop

### Program Flow

* labels
* conditional branching
* function handling

## Project Structure

```
src/
├── parser.py
├── codewriter.py
└── main.py
```

## Input Files

* BasicTest.vm
* Main.vm
* Sys.vm

## Learning Outcomes

* Stack-based computation
* VM abstraction layer
* Memory segment management
* Translation from VM code to Assembly

---

# Assignment 3 – Jack Compiler

## Overview

This assignment implements a compiler for the Jack programming language. The compiler translates Jack source code into Hack VM instructions.

A convolution program was developed and compiled using the custom compiler to validate correctness and code generation.

## Compiler Modules

### JackTokenizer

Responsible for:

* Removing comments
* Handling string constants
* Tokenizing Jack source code
* Identifying keywords, symbols, identifiers, and constants

### CompilationEngine

Responsible for:

* Recursive descent parsing
* Syntax analysis
* Parse tree generation
* VM code generation

### SymbolTable

Responsible for:

* Managing variable scope
* Tracking identifiers
* Assigning memory segments and indices

### VMWriter

Responsible for:

* Writing VM instructions
* Managing stack operations
* Generating function and control flow commands

## Project Structure

```
src/
├── JackCompiler.py
├── JackTokenizer.py
├── CompilationEngine.py
├── SymbolTable.py
└── VMWriter.py
```

## Convolution Application

The compiler was validated using a custom 2D convolution implementation.

### Features

* 3×3 convolution filter
* Matrix processing in Jack
* VM code generation
* Memory management validation
* Array access verification

### Test Cases

#### 5×5 Matrix

* Filter Size: 3×3
* Stride: 1
* Output Size: 3×3

#### 9×9 Matrix

* Filter Size: 3×3
* Stride: 1
* Output Size: 7×7

## Key Concepts

* Lexical Analysis
* Syntax Analysis
* Symbol Table Management
* VM Code Generation
* Memory Addressing
* Array Handling
* Pointer Manipulation
* Compiler Construction

---

# Technologies Used

* Python
* HDL (Hardware Description Language)
* Hack Computer Platform
* Jack Programming Language
* Virtual Machine (VM) Language

---

# How to Run

## Assignment 2

```bash
python src/main.py <input.vm>
```

## Assignment 3

```bash
python src/JackCompiler.py <JackFile.jack>
```

Generated outputs will include:

* VM code
* XML parse trees
* Tokenized XML output

---

# Author

**Mithilesh Rathod**

B.Tech Artificial Intelligence and Data Science

Indian Institute of Technology Madras

Roll Number: DA24B048
