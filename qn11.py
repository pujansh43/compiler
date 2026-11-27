
import re

# Generate Target Code
def generate_code(tac):
    code = []
    operations = {
        '+': 'ADD',
        '-': 'SUB',
        '*': 'MUL',
        '/': 'DIV'
    }

    for line in tac:
        match = re.fullmatch(
            r'(\w+)\s*=\s*(\w+)(?:\s*([+\-*/])\s*(\w+))?',
            line.strip()
        )

        if not match:
            raise ValueError("Invalid TAC: " + line)

        result, a, op, b = match.groups()

        if op:
            code += [f"MOV R0, {a}", f"MOV R1, {b}",
                     f"{operations[op]} R0, R1",
                     f"MOV {result}, R0"]
        else:
            code.append(f"MOV {result}, {a}")

    return code


# Main
print("Enter TAC (type END to finish):")
tac = []

while True:
    line = input("TAC: ").strip()
    if line.upper() == "END":
        break
    if line:
        tac.append(line)

try:
    print("\nFinal Target Code:")
    for line in generate_code(tac):
        print(line)
except ValueError as e:
    print(e)


# t1 = b * c
# t2 = a + t1
# x = t2
# END