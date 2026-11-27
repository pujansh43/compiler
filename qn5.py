# Open and read the source file directly
file = open("program.txt", "r")
code = file.read()
file.close()

keywords = [
    "int", "float", "char", "double", "void", "long", "short", 
    "signed", "unsigned", "if", "else", "while", "for", "do", 
    "switch", "case", "default", "break", "continue", "return", 
    "const", "auto", "static", "extern", "sizeof", "typedef", "struct"
]

operators = ["==", "!=", "<=", ">=", "+", "-", "*", "/", "%", "=", "<", ">"]
separators = [";", ",", "(", ")", "{", "}"]

tokens = []
i = 0
n = len(code)

while i < n:
    ch = code[i]

    # 1. Ignore whitespace and newlines
    if ch.isspace():
        i += 1

    # 2. Handle Single-Line Comments (// ...)
    elif ch == '/' and i + 1 < n and code[i+1] == '/':
        while i < n and code[i] != '\n':
            i += 1

    # 3. Handle Multi-Line Comments (/* ... */)
    elif ch == '/' and i + 1 < n and code[i+1] == '*':
        i += 2  # Skip '/*'
        while i + 1 < n and not (code[i] == '*' and code[i+1] == '/'):
            i += 1
        i += 2  # Skip '*/'

    # 4. Identify string literals ("...")
    elif ch == '"':
        lexeme = ch
        i += 1
        while i < n and code[i] != '"':
            lexeme += code[i]
            i += 1
        if i < n:
            lexeme += code[i]  # Include closing quote
            i += 1
        tokens.append((lexeme, "String Literal"))

    # 5. Identify identifiers and keywords
    elif ch.isalpha() or ch == "_":
        word = ""
        while i < n and (code[i].isalnum() or code[i] == "_"):
            word += code[i]
            i += 1
        if word in keywords:
            tokens.append((word, "Keyword"))
        else:
            tokens.append((word, "Identifier"))

    # 6. Identify numeric constants
    elif ch.isdigit():
        num = ""
        while i < n and (code[i].isdigit() or code[i] == '.'):
            num += code[i]
            i += 1
        tokens.append((num, "Constant"))

    # 7. Identify multi-character operators (e.g., ==, !=, <=, >=)
    elif i + 1 < n and code[i:i+2] in operators:
        op = code[i:i+2]
        tokens.append((op, "Operator"))
        i += 2

    # 8. Identify single-character operators (including normal division '/')
    elif ch in operators:
        tokens.append((ch, "Operator"))
        i += 1

    # 9. Identify separators
    elif ch in separators:
        tokens.append((ch, "Separator"))
        i += 1

    # 10. Skip unknown characters
    else:
        i += 1

# Display token table

print(f"{'TOKEN':<20} | {'TOKEN TYPE'}")
print("-" * 45)

for token, token_type in tokens:
    print(f"{token:<20} | {token_type}")


print(f"Total Tokens Found: {len(tokens)}")