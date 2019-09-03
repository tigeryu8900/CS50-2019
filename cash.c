#include <cs50.h>
#include <stdio.h>
#include <math.h>

#define NUM_OF_VALUES 4

// values are sorted greatest to least
#define VALUES {25, 10, 5, 1}

int main(void)
{
    int values[NUM_OF_VALUES] = VALUES;
    int change;
    
    // get user input
    do
    {
        change = round(100 * get_float("Change owed: "));
    }
    while (change < 0);
    
    // calculate number of coins
    int coins = 0;
    for (int i = 0; i < NUM_OF_VALUES; i++)
    {
        while (change >= values[i])
        {
            coins++;
            change -= values[i];
        }
    }
    
    // print the number of coins
    printf("%d\n", coins);
}
