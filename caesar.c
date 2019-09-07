#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

void badInput()
{
    printf("Usage: ./caesar key\n");
    exit(0);
}

int main(int argc, string argv[])
{
    // check key
    if (argc != 2)
    {
        badInput();
    }
    for (int i = 1; argv[1][i] != '\0'; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            badInput();
        }
    }
    
    // retrieve key
    int key = atoi(argv[1]);
    
    // retrieve plaintext and store in ciphertext
    string ciphertext = get_string("plaintext:  ");
    
    // encrypt
    for (int i = 0; ciphertext[i] != '\0'; i++)
    {
        char c = ciphertext[i];
        if (c >= 'A' && c <= 'Z')
        {
            ciphertext[i] = (((c - 'A') + key) % ('Z' - 'A' + 1)) + 'A';
        }
        else if (c >= 'a' && c <= 'z')
        {
            ciphertext[i] = (((c - 'a') + key) % ('z' - 'a' + 1)) + 'a';
        }
    }
    
    // display ciphertext
    printf("ciphertext: %s\n", ciphertext);
    
    return 0;
}
