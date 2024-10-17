import re


class ExpressionProcessor:
    def __init__(self):
        self.valid_operators = set("+-*/")

    def is_valid_expression(self, expression):
        # Удаление пробелов
        expression = expression.replace(" ", "")

        # Проверка на правильность скобок
        if not self._validate_parentheses(expression):
            return False

        # Проверка на недопустимые символы
        if not re.match(r'^[\d+\-*/()]+$', expression):
            return False

        # Проверка на неправильные последовательности операторов (например, "1+*2")
        if re.search(r'[+*/-]{2,}', expression):
            return False

        # Проверка на то, чтобы выражение не начиналось и не заканчивалось оператором
        if expression[0] in self.valid_operators or expression[-1] in self.valid_operators:
            return False

        return True

    def _validate_parentheses(self, expression):
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return len(stack) == 0

    def evaluate(self, expression):
        if not self.is_valid_expression(expression):
            raise ValueError("Invalid expression")
        try:
            return eval(expression)
        except Exception:
            raise ValueError("Invalid expression")


# Пример тестов
def run_tests():
    processor = ExpressionProcessor()

    # Корректные выражения
    valid_tests = [
        "1+2",
        "(1+2) / 3",
        "-1 + 5",
        "10 + 20 * 30",
        "100 - (50 + 25) * 2"
    ]

    # Некорректные выражения
    invalid_tests = [
        "(1+2))",  # Лишняя скобка
        "1+*6",  # Некорректные операторы
        "/3",  # Оператор в начале
        "3+",  # Оператор в конце
        "1 + a",  # Недопустимый символ 'a'
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
