
grammar = {}

n = int(input("Enter number of productions: "))

for i in range(n):
    production = input("Enter production (A->a|b): ")
    left, right = production.split("->")

    grammar[left] = right.split("|")

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


for non_terminal in grammar:
    first[non_terminal] = find_first(non_terminal)

print("\nFIRST sets:")
for symbol in grammar:
    print("FIRST(" + symbol + ") =", first[symbol])


# Enter production (A->a|b): E->TU
# Enter production (A->a|b): U->+TU|#
# Enter production (A->a|b): T->FG
# Enter production (A->a|b): G->*FG|#
# Enter production (A->a|b): F->(E)|x
