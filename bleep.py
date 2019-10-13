from cs50 import get_string
from sys import argv
import sys
import re


def main():

    if len(argv) != 2:
        sys.exit("Usage: python bleep.py dictionary")

    dictionary = set(open(argv[1]).read().split())

    message = get_string("What message would you like to censor?")

    for word in dictionary:
        message = re.sub(word, "*" * len(word), message, flags = re.IGNORECASE)

    print(message)


if __name__ == "__main__":
    main()
