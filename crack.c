#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <crypt.h>

void badInput()
{
    printf("Usage: ./crack hash\n");
    exit(1);
}

// string removeSentinel(string str)
// {
//     int length = strlen(str); 
//     char result[length];
//     int i = 0;
//     for (str[i] != '.' && i < length)
//     {
//         result[i] = str[i];
//         i++;
//     }
//     result[i] = '\0';
//     return str;
// }

bool crack(int index, string password, string hash)
{
    static string characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    static int charlen = 52;
    for (int i = 0; i < charlen; i++)
    {
        password[index] = characters[i];
        if (strcmp(crypt(password, hash), hash))
        {
            return true;
        }
        if (index < 4 && crack(index + 1, password, hash))
        {
            return true;
        }
        for (int j = 4; j > index; j++)
        {
            password[j] = '\0';
        }
    }
    return false;
}

int main(int argc, string argv[])
{
    // check hash
    if (argc != 2 || strlen(argv[1]) != 13)
    {
        badInput();
    }
    for (int i = 0; i < 13; i++)
    {
        if (!isalnum(argv[1][i]) && argv[1][i] != '.' && argv[1][i] != '/')
        {
            badInput();
        }
    }
    
    // retrieve hash
    string hash = argv[1];
    
    // permutate through all possible passwords
    string password = "\0\0\0\0\0"; // use '\0' as filler/sentinel character
    if (!crack(0, password, hash))
    {
        badInput();
    }
    printf("%s\n", password);
    return 0;
}
