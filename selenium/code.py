import streamlit as st
import pandas as pd
from datetime import datetime
import io
import contextlib

if 'code_storage' not in st.session_state:
    st.session_state.code_storage = []

if 'selected_code' not in st.session_state:
    st.session_state.selected_code = '' 

def run_code(code):
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code)
        result = output.getvalue()
    except Exception as e:
        result = f"Error: {str(e)}"
    return result

def save_code(name, code):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.code_storage.append({'name': name, 'code': code, 'date': timestamp})

def delete_code(index):
    st.session_state.code_storage.pop(index)

code_input = st.text_area("Enter your code here:", st.session_state.selected_code)


if st.button("Run"):
    if code_input.strip():
        result = run_code(code_input)
        st.text_area("Output", result) 

if 'show_name_input' not in st.session_state:
    st.session_state.show_name_input = False

if st.button("Save Code"):
    if code_input.strip():
        st.session_state.show_name_input = True  

if st.session_state.show_name_input:
    code_name = st.text_input("Enter a name for your code:")
    if st.button("Confirm Save"):
        if code_name.strip(): 
            save_code(code_name, code_input)
            st.success("Code saved!")
            st.session_state.show_name_input = False 
        else:
            st.error("Please enter a valid code name.")

if st.session_state.code_storage:
    st.subheader("Saved Codes")
    for i, code_entry in enumerate(st.session_state.code_storage):
        col1, col2, col3 = st.columns([2, 2, 1])
        if col1.button(code_entry['name'], key=f"load_{i}"):
            st.session_state.selected_code = code_entry['code']  

        col2.write(code_entry['date'])
        delete_button = col3.button("Delete", key=f"delete_{i}")

        if delete_button:
            delete_code(i)
