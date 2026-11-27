# Open and read the source file directly without try-except
file = open("program.txt", "r")
code = file.read()
file.close()

# Expanded list of keywords
keywords = [
    "int", "float", "char", "double", "void", "long", "short", 
    "signed", "unsigned", "if", "else", "while", "for", "do", 
    "switch", "case", "default", "break", "continue", "return", 
    "const", "auto", "static", "extern", "sizeof", "typedef", "struct"
]

operators = ["==", "!=", "<=", ">=", "+", "-", "*", "/", "%", "=", "<", ">"]
separators = [";", ",", "(", ")", "{", "}"]

# Variable to store all analyzed tokens
tokens = []
i = 0

# Scan source code character by character
while i < len(code):
    ch = code[i]

    # 1. Ignore whitespace and newlines
    if ch.isspace():
        i += 1

    # 2. Identify strings ("...")
    elif ch == '"':
        lexeme = ch
        i += 1
        while i < len(code) and code[i] != '"':
            lexeme += code[i]
            i += 1
        if i < len(code):
            lexeme += code[i]  # closing quote
            i += 1
        tokens.append((lexeme, "String Literal"))

    # 3. Identify identifiers and keywords
    elif ch.isalpha() or ch == "_":
        word = ""
        while i < len(code) and (code[i].isalnum() or code[i] == "_"):
            word += code[i]
            i += 1

        # Check classification against the expanded keyword list
        if word in keywords:
            tokens.append((word, "Keyword"))
        else:
            tokens.append((word, "Identifier"))

    # 4. Identify numbers (Constants)
    elif ch.isdigit():
        num = ""
        while i < len(code) and (code[i].isdigit() or code[i] == '.'):
            num += code[i]
            i += 1
        tokens.append((num, "Constant"))

    # 5. Identify multi-character and single-character operators
    elif i + 1 < len(code) and code[i:i+2] in operators:
        op = code[i:i+2]
        tokens.append((op, "Operator"))
        i += 2
    elif ch in operators:
        tokens.append((ch, "Operator"))
        i += 1

    # 6. Identify separators
    elif ch in separators:
        tokens.append((ch, "Separator"))
        i += 1

    # 7. Ignore unknown characters
    else:
        i += 1

# Display token table
print("\nTOKEN\t\t\tTOKEN TYPE")
print("-" * 45)

for token, token_type in tokens:
    print(f"{token:<20} \t {token_type}")