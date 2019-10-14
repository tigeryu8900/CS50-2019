from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    a = a.split('\n')
    b = b.split('\n')
    result = []
    for i in range(len(a)):
        for j in range(i, len(b)):
            if a[i] == b[j]:
                result.append(a[i])

    return result


def sentences(a, b):
    """Return sentences in both a and b"""

    a = sent_tokenize(a)
    b = sent_tokenize(b)
    result = []
    for i in range(len(a)):
        for j in range(i, len(b)):
            if a[i] == b[j]:
                result.append(a[i])

    return result


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    result = []
    for i in range(len(a) - n):
        if b.find(a[i : i + n]) > -1:
            result.append(a[i : i + n])

    return result
