import re

class ExpressionProcessor:
    def __init__(self):
        self.valid_operators = set("+-*/")
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    
    def is_valid_expression(self, expression):
        # Удаление пробелов
        expression = expression.replace(" ", "")
        
        # Проверка на корректность скобок
        if expression.count('(') != expression.count(')'):
            return False
        
        # Проверка на допустимые символы
        if not re.match(r'^[\d+\-*/()]+$', expression):
            return False
        
        # Проверка на корректность оператора
        if re.search(r'[+\-*/]{2,}', expression):  # два или более оператора подряд
            return False
        
        # Проверка на операторы в начале или в конце
        if expression[0] in self.valid_operators or expression[-1] in self.valid_operators:
            return False
        
        return True

    def evaluate(self, expression):
        if not self.is_valid_expression(expression):
            raise ValueError("Invalid expression")
        
        values = []  # Стек для чисел
        operators = []  # Стек для операторов
        tokens = re.findall(r'\d+|[-+*/()]', expression)  # Разделение на токены
        
        for token in tokens:
            if token.isdigit():  # Если токен - число
                values.append(int(token))
            elif token in self.valid_operators:  # Если токен - оператор
                while (operators and operators[-1] != '(' and
                       self.precedence[token] <= self.precedence[operators[-1]]):
                    self.apply_operator(values, operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self.apply_operator(values, operators.pop())
                operators.pop()  # Удаляем '(' из стека
        
        while operators:
            self.apply_operator(values, operators.pop())
        
        return values[0]

    def apply_operator(self, values, operator):
        b = values.pop()
        a = values.pop()
        if operator == '+':
            values.append(a + b)
        elif operator == '-':
            values.append(a - b)
        elif operator == '*':
            values.append(a * b)
        elif operator == '/':
            values.append(a / b)

def run_tests():
    processor = ExpressionProcessor()

    valid_tests = [
        "1+2",
        "(1+2) / 3",
        "-1 + 5",
        "10 + 20 * 30",
        "100 - (50 + 25) * 2"
    ]

    invalid_tests = [
        "(1+2))",  # Лишняя скобка
        "1+*6",  # Некорректные операторы
        "/3",  # Оператор в начале
        "3+",  # Оператор в конце
        "1 + a",  # Недопустимый символ
        "1 + 2 ** 3"  # Некорректный оператор **
    ]

    print("Valid expressions:")
    for expression in valid_tests:
        try:
            result = processor.evaluate(expression)
            print(f"{expression} = {result}")
        except ValueError as e:
            print(f"{expression} failed: {str(e)}")

    print("\nInvalid expressions:")
    for expression in invalid_tests:
        try:
            result = processor.evaluate(expression)
            print(f"Error: {expression} should not have passed!")
        except ValueError as e:
            print(f"{expression} failed as expected: {str(e)}")

run_tests()
