
import re

grammar = {}
n = int(input("Enter number of productions: "))

for _ in range(n):
    p = input("Enter production: ")
    left, right = p.split("->")
    grammar.setdefault(left, []).extend(re.split(r'\|', right))

start = list(grammar.keys())[0]
NT = set(grammar)

# Convert grammar into productions
P = [(a, b.replace('#', '')) for a in grammar for b in grammar[a]]

# Calculate FIRST sets
first = {a: set() for a in NT}

changed = True
while changed:
    changed = False
    for a, b in P:
        result = set()
        nullable = True

        for ch in b:
            if ch not in NT:
                result.add(ch)
                nullable = False
                break
            result.update(first[ch] - {'#'})
            if '#' not in first[ch]:
                nullable = False
                break

        if nullable:
            result.add('#')

        old = len(first[a])
        first[a].update(result)
        if len(first[a]) > old:
            changed = True


def first_string(s):
    result = set()
    for ch in s:
        if ch not in NT:
            result.add(ch)
            return result
        result.update(first[ch] - {'#'})
        if '#' not in first[ch]:
            return result
    result.add('#')
    return result


# Calculate FOLLOW sets
follow = {a: set() for a in NT}
follow[start].add('$')

changed = True
while changed:
    changed = False
    for a, b in P:
        for i, ch in enumerate(b):
            if ch in NT:
                temp = first_string(b[i+1:])
                old = len(follow[ch])
                follow[ch].update(temp - {'#'})
                if '#' in temp:
                    follow[ch].update(follow[a])
                if len(follow[ch]) > old:
                    changed = True


# Augment grammar
aug = start + "'"
while aug in NT:
    aug += "'"

P.insert(0, (aug, start))
NT.add(aug)

# CLOSURE function
def closure(items):
    items = set(items)
    changed = True

    while changed:
        changed = False
        for i, dot in list(items):
            a, b = P[i]
            if dot < len(b) and b[dot] in NT:
                x = b[dot]
                for j, (c, d) in enumerate(P):
                    if c == x and (j, 0) not in items:
                        items.add((j, 0))
                        changed = True
    return frozenset(items)


# GOTO function
def goto(items, x):
    result = set()
    for i, dot in items:
        a, b = P[i]
        if dot < len(b) and b[dot] == x:
            result.add((i, dot + 1))
    return closure(result) if result else frozenset()


# Construct LR(0) states
states = [closure({(0, 0)})]
trans = {}

i = 0
symbols = sorted(NT | {
    ch for a, b in P for ch in b if ch not in NT
})

while i < len(states):
    for x in symbols:
        new = goto(states[i], x)
        if new:
            if new not in states:
                states.append(new)
            trans[i, x] = states.index(new)
    i += 1


# Construct ACTION and GOTO tables
ACTION = {}
GOTO = {}
conflict = False

def add(table, key, value):
    global conflict
    if key in table and table[key] != value:
        print("Conflict at", key)
        conflict = True
    else:
        table[key] = value


for i, I in enumerate(states):
    for j, dot in I:
        a, b = P[j]

        if dot < len(b):
            x = b[dot]
            if x not in NT:
                add(ACTION, (i, x), "s" + str(trans[i, x]))
        else:
            if j == 0:
                add(ACTION, (i, '$'), "acc")
            else:
                for x in follow[a]:
                    add(ACTION, (i, x), "r" + str(j))

    for x in NT - {aug}:
        if (i, x) in trans:
            GOTO[i, x] = trans[i, x]


# Display parsing table
terminals = sorted({ch for a, b in P for ch in b if ch not in NT} | {'$'})
nonterminals = sorted(NT - {aug})

print("\nSLR(1) Parsing Table")
print("State\t" + "\t".join(terminals + nonterminals))

for i in range(len(states)):
    print(i, end="\t")
    for x in terminals:
        print(ACTION.get((i, x), "-"), end="\t")
    for x in nonterminals:
        print(GOTO.get((i, x), "-"), end="\t")
    print()


# Check input string
if not conflict:
    print("\nGrammar is SLR(1)")
    s = input("\nEnter input string: ") + "$"
    stack = [0]
    i = 0

    while True:
        action = ACTION.get((stack[-1], s[i]))

        if action is None:
            print("String Rejected")
            break

        if action == "acc":
            print("String Accepted")
            break

        elif action[0] == 's':
            stack.append(int(action[1:]))
            i += 1

        elif action[0] == 'r':
            j = int(action[1:])
            a, b = P[j]

            if b:
                del stack[-len(b):]

            state = stack[-1]
            stack.append(GOTO[state, a])

else:
    print("\nGrammar is not SLR(1)")
