import streamlit as st
import pandas as pd
from datetime import datetime
import io
import contextlib

# Инициализация состояния для сохраненных кодов
if 'code_storage' not in st.session_state:
    st.session_state.code_storage = []

if 'selected_code' not in st.session_state:
    st.session_state.selected_code = ''  # Для хранения выбранного кода

# Функция для выполнения кода и перехвата вывода
def run_code(code):
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code)
        result = output.getvalue()
    except Exception as e:
        result = f"Error: {str(e)}"
    return result

# Функция для сохранения кода
def save_code(name, code):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.code_storage.append({'name': name, 'code': code, 'date': timestamp})

# Функция для удаления кода
def delete_code(index):
    st.session_state.code_storage.pop(index)

# Интерфейс страницы
st.title("Code Runner with Save Feature")

# Если пользователь выбрал сохраненный код, показываем его в текстовом поле
code_input = st.text_area("Enter your Python code here:", st.session_state.selected_code)

# Кнопка для запуска кода
if st.button("Run"):
    if code_input.strip():
        result = run_code(code_input)
        st.text_area("Output", result)  # Отображаем результат выполнения

# Инициализация состояния для хранения имени кода
if 'show_name_input' not in st.session_state:
    st.session_state.show_name_input = False

# Кнопка для сохранения кода
if st.button("Save Code"):
    if code_input.strip():  # Проверка, что код не пустой
        st.session_state.show_name_input = True  # Показать поле для ввода имени

# Если нажата кнопка "Save Code", показываем поле для ввода имени
if st.session_state.show_name_input:
    code_name = st.text_input("Enter a name for your code:")
    if st.button("Confirm Save"):
        if code_name.strip():  # Проверка, что имя не пустое
            save_code(code_name, code_input)
            st.success("Code saved!")
            st.session_state.show_name_input = False  # Скрыть поле после сохранения
        else:
            st.error("Please enter a valid code name.")

# Отображение сохраненных кодов в виде таблицы
if st.session_state.code_storage:
    st.subheader("Saved Codes")
    for i, code_entry in enumerate(st.session_state.code_storage):
        col1, col2, col3 = st.columns([2, 2, 1])
        # Добавляем возможность кликнуть на имя кода, чтобы он отобразился в текстовом поле
        if col1.button(code_entry['name'], key=f"load_{i}"):
            st.session_state.selected_code = code_entry['code']  # Загружаем код в текстовое поле

        col2.write(code_entry['date'])
        delete_button = col3.button("Delete", key=f"delete_{i}")

        # Удаление кода
        if delete_button:
            delete_code(i)
