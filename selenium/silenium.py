from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Укажите путь к ChromeDriver
service = Service("D:/Veronika/lab2/code.py")  # Замените на ваш путь к ChromeDriver

# Настройки для Chrome
driver = webdriver.Chrome(service=service)

# Открываем веб-страницу
driver.get("http://localhost:8501")  # Если тестируете локальное приложение (например, Streamlit)

# Ждём, пока страница загрузится
time.sleep(3)

# Найти поле для ввода кода
code_input = driver.find_element(By.XPATH, "//textarea[@aria-label='Enter your Python code here:']")

# Вводим текст в поле
code_input.send_keys("print('Hello, World!')")

# Нажимаем на кнопку "Run"
run_button = driver.find_element(By.XPATH, "//button[contains(text(),'Run')]")
run_button.click()

# Ждём выполнения кода
time.sleep(2)

# Проверка результата
output = driver.find_element(By.XPATH, "//textarea[@aria-label='Output']")
assert "Hello, World!" in output.get_attribute('value')

# Закрыть браузер
driver.quit()
