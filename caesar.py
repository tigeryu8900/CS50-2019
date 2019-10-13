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
ciphertext = list(get_string("plaintext:  "))

# encrypt
for i in range(len(ciphertext)):
    c = ord(ciphertext[i])
    if ord('A') <= c <= ord('Z'):
        ciphertext[i] = chr((((c - ord('A')) + key) % (ord('Z') - ord('A') + 1)) + ord('A'))
    elif ord('a') <= c <= ord('z'):
        ciphertext[i] = chr((((c - ord('a')) + key) % (ord('z') - ord('a') + 1)) + ord('a'))

# display ciphertext
print("ciphertext: ".join(ciphertext));
