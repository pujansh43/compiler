
import re

precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

# Infix to Postfix
def infix_to_postfix(expr):
    tokens = re.findall(r'[a-zA-Z_]\w*|\d+|[()+\-*/]', expr)

    if not expr.strip() or ''.join(tokens) != re.sub(r'\s+', '', expr):
        raise ValueError("Invalid expression")

    output, stack = [], []

    for token in tokens:
        if re.fullmatch(r'[a-zA-Z_]\w*|\d+', token):
            output.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Unmatched parentheses")
            stack.pop()

        else:
            while stack and stack[-1] != '(' and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)

    while stack:
        if stack[-1] == '(':
            raise ValueError("Unmatched parentheses")
        output.append(stack.pop())

    return output


# Generate Three Address Code
def generate_tac(postfix):
    stack, code = [], []
    count = 1

    for token in postfix:
        if token not in precedence:
            stack.append(token)
        else:
            if len(stack) < 2:
                raise ValueError("Invalid expression")

            b, a = stack.pop(), stack.pop()
            temp = f"t{count}"
            count += 1

            code.append(f"{temp} = {a} {token} {b}")
            stack.append(temp)

    if len(stack) != 1:
        raise ValueError("Invalid expression")

    return code, stack[0]


# Main
try:
    expr = input("Enter arithmetic expression: ")
    postfix = infix_to_postfix(expr)
    tac, result = generate_tac(postfix)

    print("\nThree Address Code:")
    for line in tac:
        print(line)
    print("Result =", result)

except ValueError as e:
    print("Invalid Expression:", e)

# (a+b)*c-d