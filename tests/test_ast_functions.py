from autodocs.core.main import parse_file, write_file
from autodocs.core.function import FunctionDocStringAnnotator

import pytest
import libcst as cst

import os

def test_function_single():
    tree = parse_file("tests/data/0.py")
    gen = FunctionDocStringAnnotator(tree.default_indent)
    write_file("tests/output/0.py", tree.visit(gen))

def test_exception_detection():
    code = """
def test1():
    raise ValueError
    raise ValueError("Test1")
    raise Exception.ValueError
    raise Exception.ValueError("Test2")
"""

    tree = cst.parse_module(code)
    annotator = FunctionDocStringAnnotator(tree.default_indent)
    write_file("tests/output/test_exception_detection.py", tree.visit(annotator))

def test_function_batch():
    from random import randint
    
    n = 30
    for _ in range(n):
        i = randint(0, 33736)
        file = f"tests/data/{i}.py"
        if os.path.exists(file):
            tree = parse_file(file)
            annotator = FunctionDocStringAnnotator(tree.default_indent)
            write_file(f"tests/output/{i}.py",  tree.visit(annotator))

@pytest.mark.skip
def test_v0_1():
    pass