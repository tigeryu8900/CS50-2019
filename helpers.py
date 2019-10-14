from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    a = a.split('\n')
    b = b.split('\n')
    result = set()
    for i in a:
        for j in b:
            if i == j:
                result.add(a)

    return list(result)


def sentences(a, b):
    """Return sentences in both a and b"""

    a = sent_tokenize(a)
    b = sent_tokenize(b)
    result = set()
    for i in a:
        for j in b:
            if i == j:
                result.add(i)

    return list(result)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    result = set()
    for i in range(len(a) - n + 1):
        if b.find(a[i : i + n]) > -1:
            result.add(a[i : i + n])

    return list(result)
