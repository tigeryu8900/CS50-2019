#include <cs50.h>
#include <stdio.h>
#include <math.h>

void invalid()
{
    printf("INVALID\n");
    exit(0);
}

int main(void)
{
    long number;
    string type;

    // get user input
    number = get_long("Number: ");

    // classify number
    long identifier = number;
    while (identifier > 99)
    {
        identifier /= 10;
    }
    switch (identifier / 10)
    {
        case 3:
            switch (identifier % 10)
            {
                case 4:
                case 7:
                    type = "AMEX\n";
                    break;
                default:
                    invalid();
            }
            break;
        case 4:
            type = "VISA\n";
            break;
        case 5:
            switch (identifier % 10)
            {
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                    type = "MASTERCARD\n";
                    break;
                default:
                    invalid();
            }
            break;
        default:
            invalid();
    }

    // verify number
    int checksum = 0;
    long tempNumber = number / 10;
    while (tempNumber > 0)
    {
        int product = 2 * (tempNumber % 10);
        while (product > 0)
        {
            checksum += product % 10;
            product /= 10;
        }
        tempNumber /= 100;
    }
    tempNumber = number;
    while (tempNumber > 0)
    {
        checksum += tempNumber % 10;
        tempNumber /= 100;
    }
    if (checksum % 10 != 0 || checksum == 40)
    {
        invalid();
    }

    // print type
    printf("%d%s", checksum, type);
}
