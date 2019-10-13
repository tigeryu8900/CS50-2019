import sys

from cs50 import get_float

NUM_OF_VALUES = 4

# values are sorted greatest to least
values = [25, 10, 5, 1]

# get user input
change = round(100 * get_float("Change owed: "))
while (change < 0):
    change = round(100 * get_float("Change owed: "))

# calculate number of coins
coins = 0
for i in range(NUM_OF_VALUES):
    while change >= values[i]:
        coins += 1
        change -= values[i]

# print the number of coins
print(coins)
