
s = input("Enter a string: ")

# Check a*
flag1 = True

for ch in s:
    if ch != 'a':
        flag1 = False
        break

if flag1:
    print("Valid under a*")
else:
    print("Invalid under a*")


# Check a*b+
flag2 = True
i = 0

# Check zero or more a's
while i < len(s) and s[i] == 'a':
    i += 1

# Check one or more b's
if i == len(s):
    flag2 = False
else:
    while i < len(s) and s[i] == 'b':
        i += 1

    if i != len(s):
        flag2 = False

if flag2:
    print("Valid under a*b+")
else:
    print("Invalid under a*b+")


# Check abb
if (s == "abb"):
    print("Valid under abb")
else:
    print("Invalid under abb")
