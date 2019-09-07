#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

void badInput()
{
    printf("Usage: ./vigenere keyword\n");
    exit(1);
}

int main(int argc, string argv[])
{
    // check keyword
    if (argc != 2)
    {
        badInput();
    }
    for (int i = 1; argv[1][i] != '\0'; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            badInput();
        }
    }
    
    // retrieve keyword
    string keyword = argv[1];
    
    // retrieve keyword length
    int keywordLength;
    for (keywordLength = 0; keyword[keywordLength] != '\0'; keywordLength++);
    
    // retrieve key array
    int keyArray[keywordLength];
    for (int i = 0; i < keywordLength; i++)
    {
        keyArray[i] = islower(keyword[i])
                      ? ((keyword[i] - 'a') % ('z' - 'a' + 1))
                      : ((keyword[i] - 'A') % ('Z' - 'A' + 1));
    }
    
    // retrieve plaintext and store in ciphertext
    string ciphertext = get_string("plaintext:  ");
    
    // encrypt
    for (int i = 0; ciphertext[i] != '\0'; i++)
    {
        if (isalpha(ciphertext[i]))
        {
            ciphertext[i] = islower(ciphertext[i])
                            ? (((ciphertext[i] - 'a' + keyArray[i % keywordLength])
                                % ('z' - 'a' + 1)) + 'a')
                            : (((ciphertext[i] - 'A' + keyArray[i % keywordLength])
                                % ('Z' - 'A' + 1)) + 'A');
        }
    }
    
    // display ciphertext
    printf("ciphertext: %s\n", ciphertext);
    
    return 0;
}
