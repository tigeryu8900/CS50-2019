from sys import argv

from crypt import crypt


def badInput():
    sys.exit("Usage: ./crack hash")

# // string removeSentinel(string str)
# // {
# //     int length = strlen(str);
# //     char result[length];
# //     int i = 0;
# //     for (str[i] != '.' && i < length)
# //     {
# //         result[i] = str[i];
# //         i++;
# //     }
# //     result[i] = '\0';
# //     return str;
# // }


characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
charlen = len(characters)


def crack(index, password, h):
    for c in characters:
        password[index] = c
        for j in range(index + 1, 5):
            password[j] = '\0'
# //         if (strlen(password) == 3)
# //         {
# //             printf("%s\n", password);
# //         }
        if crypt("".join(password).replace("\0", ""), h) == h:
            return True
        if index < 4 and crack(index + 1, password, h):
            return True
    return False


# check hash
if len(argv) != 2 or len(argv[1]) != 13:
    badInput()
# for i in range(13):
#     if (!isalnum(argv[1][i]) && argv[1][i] != '.' && argv[1][i] != '/'):
#         badInput()

# retrieve hash
h = argv[1]

# permutate through all possible passwords
password = list("\0\0\0\0\0")
# //     printf("LOL hash: %s", crypt("LOL", "50cI2vYkF0YU2"));
if not crack(0, password, h):
    badInput()

print("".join(password))
