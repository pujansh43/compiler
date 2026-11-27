
import re

grammar = {}

n = int(input("Enter number of productions: "))

for _ in range(n):
    p = input("Enter production: ")
    left, right = p.split("->")
    grammar[left] = re.split(r'\|', right)

# Calculate FIRST sets
first = {nt: set() for nt in grammar}

changed = True
while changed:
    changed = False

    for nt in grammar:
        for prod in grammar[nt]:
            temp = first_string(prod) if False else None

            if prod == '#':
                symbols = {'#'}
            else:
                symbols = set()
                for ch in prod:
                    if ch not in grammar:
                        symbols.add(ch)
                        break
                    symbols.update(first[ch] - {'#'})
                    if '#' not in first[ch]:
                        break
                else:
                    symbols.add('#')

            old = len(first[nt])
            first[nt].update(symbols)
            if len(first[nt]) > old:
                changed = True


def first_string(s):
    result = set()

    for ch in s:
        if ch not in grammar:
            result.add(ch)
            return result

        result.update(first[ch] - {'#'})

        if '#' not in first[ch]:
            return result

    result.add('#')
    return result


# Calculate FOLLOW sets
follow = {nt: set() for nt in grammar}
start = list(grammar.keys())[0]
follow[start].add('$')

changed = True
while changed:
    changed = False

    for left in grammar:
        for prod in grammar[left]:
            for i, ch in enumerate(prod):
                if ch in grammar:
                    temp = first_string(prod[i+1:])
                    old = len(follow[ch])

                    follow[ch].update(temp - {'#'})

                    if '#' in temp:
                        follow[ch].update(follow[left])

                    if len(follow[ch]) > old:
                        changed = True


# Construct parsing table
table = {nt: {} for nt in grammar}
ll1 = True

for left in grammar:
    for prod in grammar[left]:
        temp = first_string(prod)

        for t in temp - {'#'}:
            if t in table[left]:
                ll1 = False
                print("Conflict at M[", left, ",", t, "]")
            else:
                table[left][t] = prod

        if '#' in temp:
            for t in follow[left]:
                if t in table[left]:
                    ll1 = False
                    print("Conflict at M[", left, ",", t, "]")
                else:
                    table[left][t] = prod


# Display parsing table
terminals = set('$')

for prods in grammar.values():
    for prod in prods:
        terminals.update(ch for ch in prod
                         if ch not in grammar and ch != '#')

terminals = sorted(terminals)

print("\nLL(1) Parsing Table")
print("NT\t" + "\t".join(terminals))

for nt in grammar:
    print(nt, end="\t")
    for t in terminals:
        print(table[nt].get(t, "-"), end="\t")
    print()


# Check input string
if ll1:
    print("\nGrammar is LL(1)")

    s = input("\nEnter input string: ") + "$"
    stack = ["$", start]
    i = 0

    while stack:
        top = stack[-1]

        if top == '$' and s[i] == '$':
            print("String Accepted")
            break

        if top not in grammar:
            if top == s[i]:
                stack.pop()
                i += 1
            else:
                print("String Rejected")
                break
        else:
            prod = table[top].get(s[i])

            if prod is None:
                print("String Rejected")
                break

            stack.pop()
            if prod != '#':
                stack.extend(reversed(prod))

else:
    print("\nGrammar is not LL(1)")



# Enter production (A->a|b): E->TU
# Enter production (A->a|b): U->+TU|#
# Enter production (A->a|b): T->FG
# Enter production (A->a|b): G->*FG|#
# Enter production (A->a|b): F->(E)|x

# x+(x*x) x+x*x
# x+x) x++x



# E->E+T|T
# T->T*F|F
# F->(E)|x

# x+x*x (x)
# (x+x ()