def div(a,b):
    if b==0:
        raise ValueError("Cannot divide by zero")
    return (a/b)


# a = float(input("Enter first number: "))
# b = float(input("Enter second number: "))
# try:
#     c = div(a,b)
#     print(f"The div of {a} and {b} is {c}")
# except ValueError as e:
#     print(f"Error:{e}")

# Unit tests have been moved to test_addition.py
