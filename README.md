# Mini LISP

> NCU 2024 Compiler Final Project

This project aims to implement a simplified version of Lisp, called Mini-Lisp, which is an interpreter.

- [More about Final Project](Compiler%20Final%20Project/Compiler%20Final%20Project.pdf)
- [More about Mini-Lisp](Compiler%20Final%20Project/MiniLisp.pdf)

## Environment

- python 3.9 or above

- dependencies:

```shell
pip install ply
```

## How to run

### 1. Set Test Data Directory 
Make sure to have a directory named `test_data`.\
In the `test_data` directory, there should be multiple files with the .lsp extension, serving as input for this Mini-Lisp.
### 2. Run miniLisp.py
```shell
python miniLisp.py
```

## Features

### Basic Features

- [x] Syntax Validation
- [x] Print
- [x] Numerical Operations
- [x] Logical Operations
- [x] if Expression
- [x] Variable Definition
- [x] Function
- [x] Named Function

### Bonus Features

- [x] Recursion
- [x] Type Checking
- [x] Nested Function
- [x] First-class Function

## Examples (Function Feature)
### Input
```
(define foo
  (fun (a b c) (+ a b (* b c))))

(print-num (foo 10 9 8))
```
### Output
`91`