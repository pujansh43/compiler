
grammar = {}

n = int(input("Enter number of productions: "))

for i in range(n):
    production = input("Enter production (A->a|b): ")
    left, right = production.split("->")

    if left not in grammar:
        grammar[left] = []

    grammar[left].extend(right.split("|"))

# Calculate FIRST sets
first = {}

def find_first(symbol):
    if symbol not in grammar:
        return {symbol}

    if symbol in first:
        return first[symbol]

    result = set()

    for production in grammar[symbol]:
        if production == '#':
            result.add('#')
            continue

        for char in production:
            temp = find_first(char)
            result.update(temp - {'#'})

            if '#' not in temp:
                break
        else:
            result.add('#')

    first[symbol] = result
    return result


# Calculate FIRST of a string
def first_string(string):
    result = set()

    if string == "":
        return {'#'}

    for char in string:
        temp = find_first(char)
        result.update(temp - {'#'})

        if '#' not in temp:
            break
    else:
        result.add('#')

    return result


# Initialize FOLLOW sets
follow = {nt: set() for nt in grammar}

start = list(grammar.keys())[0]
follow[start].add('$')

# Calculate FOLLOW sets
changed = True

while changed:
    changed = False

    for left in grammar:
        for production in grammar[left]:

            for i in range(len(production)):
                symbol = production[i]

                if symbol in grammar:
                    before = len(follow[symbol])

                    remaining = production[i + 1:]
                    temp = first_string(remaining)

                    follow[symbol].update(temp - {'#'})

                    if '#' in temp:
                        follow[symbol].update(follow[left])

                    if len(follow[symbol]) > before:
                        changed = True


# Display FOLLOW sets
print("\nFOLLOW Sets:")

for nt in grammar:
    print("FOLLOW(" + nt + ") =", follow[nt])
