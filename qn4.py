
identifier = input("Enter an identifier: ")

keywords = [
    "auto", "break", "case", "char", "const",
    "continue", "default", "do", "double", "else",
    "enum", "extern", "float", "for", "goto",
    "if", "int", "long", "register", "return",
    "short", "signed", "sizeof", "static", "struct",
    "switch", "typedef", "union", "unsigned",
    "void", "volatile", "while"
]

flag = True

# Check whether identifier is empty
if len(identifier) == 0:
    flag = False

# Check first character
elif not (identifier[0].isalpha() or identifier[0] == '_'):
    flag = False

else:
    # Check remaining characters
    for ch in identifier:
        if not (ch.isalnum() or ch == '_'):
            flag = False
            break

# Check reserved keywords
if identifier in keywords:
    flag = False

if flag:
    print("Valid Identifier")
else:
    print("Invalid Identifier")
