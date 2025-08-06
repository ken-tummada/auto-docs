import streamlit as st
import libcst as cst

from autodocs.core.function import FunctionDocStringAnnotator

st.title("Scrollable Python File Viewer")

uploaded_file = st.file_uploader("Upload a Python file", type=["py"])

if uploaded_file is not None:
    source_code = uploaded_file.read().decode("utf-8")
    source_module = cst.parse_module(source_code)
    annotator = FunctionDocStringAnnotator(source_module.default_indent)
    annotated_module = source_module.visit(annotator)
    st.code(annotated_module.code, language="python", height=600, wrap_lines=True, line_numbers=True)