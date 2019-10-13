import sys

from cs50 import get_string


def badInput():
    sys.exit("Usage: python caesar.py key")

# check key
if len(sys.argv) != 2:
    badInput()

if not sys.argv[1].isnumeric():
    badInput()

# retrieve key
key = int(sys.argv[1])

# retrieve plaintext and store in ciphertext
ciphertext = get_string("plaintext:  ")

# encrypt
a = ord(a)
z = ord(z)
A = ord(A)
Z = ord(Z)
for i in range(len(ciphertext)):
    c = ord(ciphertext[i])
    if A <= c <= Z:
        ciphertext[i] = chr((((c - A) + key) % (Z - A + 1)) + A)
    elif a <= c <= z:
        ciphertext[i] = chr((((c - a) + key) % (z - a + 1)) + a)

# display ciphertext
print("ciphertext:", ciphertext);
