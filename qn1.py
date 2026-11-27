
comment = input("Enter a comment: ")

# Check single-line comment
if len(comment) >= 2 and comment[0] == '/' and comment[1] == '/':
    print("Valid Single-line Comment")

# Check multi-line comment
elif (len(comment) >= 4 and
      comment[0] == '/' and comment[1] == '*' and
      comment[-2] == '*' and comment[-1] == '/'):

    print("Valid Multi-line Comment")

else:
    print("Invalid Comment")
