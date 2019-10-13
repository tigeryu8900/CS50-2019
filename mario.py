import sys

from cs50 import get_int

# get user input
height = get_int("Height: ")
while height < 1 or height > 8:
    height = get_int("Height: ")

# make pyramid
for i in range(height):
    print(" " * (height - i - 1) + "#" * (i + 1))
