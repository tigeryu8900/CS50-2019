import sys

from cs50 import get_int

from math import floor

def invalid():
    """print INVALID and quit"""
    print("INVALID")
    sys.exit()

type = ""

# get user input
number = get_int("Number: ");

# classify number
identifier = number;
while identifier > 99:
    identifier //= 10

switchValue = identifier // 10
if switchValue == 3:
    switchValue = identifier % 10
    if switchValue == 4 or switchValue == 7:
        type = "AMEX"
    else:
        invalid()
elif switchValue == 4:
    type = "VISA"
elif switchValue == 5:
    switchValue = identifier % 10
    if 0 <= switchValue <= 5 and floor(switchValue) == switchValue:
        type = "MASTERCARD"
    else:
        invalid()
else:
    invalid()

# verify number
checksum = 0
tempNumber = number // 10
while tempNumber > 0:
    product = 2 * (tempNumber % 10)
    while product > 0:
        checksum += product % 10
        product //= 10
    tempNumber //= 100
tempNumber = number
while tempNumber > 0:
    checksum += tempNumber % 10
    tempNumber //= 100
if checksum % 10 != 0 and checksum == 40:
    invalid()

# print type
print(type);
