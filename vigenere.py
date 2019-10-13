import sys

from cs50 import get_string


def badInput():
    sys.exit("Usage: python vigenere.py keyword")


# check key
if len(sys.argv) != 2:
    badInput()

if not sys.argv[1].isalpha():
    badInput()

# retrieve keyword
keyword = list(sys.argv[1])

# retrieve plaintext and store in ciphertext
ciphertext = list(get_string("plaintext:  "))

keyArray = []
for c in keyword:
    keyArray.append(((ord(c) - ord('A')) % (ord('Z') - ord('A') + 1),
                     (ord(c) - ord('a')) % (ord('z') - ord('a') + 1))
                    [c.islower()])


# encrypt
j = 0
for i in range(len(ciphertext)):
    if ciphertext[i].isalpha():
        ciphertext[i] = chr(
            (((ord(ciphertext[i]) - ord('A') + keyArray[j % len(keyword)]) % (ord('Z') - ord('A') + 1)) + ord('A'),
             ((ord(ciphertext[i]) - ord('a') + keyArray[j % len(keyword)]) % (ord('z') - ord('a') + 1)) + ord('a'))
            [ciphertext[i].islower()])
        j += 1

# display ciphertext
print("ciphertext:", "".join(ciphertext))
