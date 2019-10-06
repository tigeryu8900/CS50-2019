#include <stdio.h>
#include <stdlib.h>

typedef unsigned char byte;

// checks whether the block is the first block of an image
int isStartOfImage(byte *data)
{
    return data[0] == 0xff && data[1] == 0xd8 && data[2] == 0xff && (data[3] & 0xf0) == 0xe0;
}

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // remember filenames
    char *image = argv[1];

    // open input file
    FILE *inptr = fopen(image, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", image);
        return 2;
    }

    // create output file pointer
    FILE *outptr = NULL;

    // iterate through bytes
    int fileCount = 0;
    byte block[512];
    while (1 == fread(block, 512, 1, inptr))
    {
        // check whether the block is the first block of an image
        if (isStartOfImage(block))
        {
            // close the previous file if outptr is opened
            if (outptr != NULL)
            {
                fclose(outptr);
            }
            // open a new image file
            char fname[8];
            sprintf(fname, "%03d.jpg", fileCount++);
            outptr = fopen(fname, "w");
        }
        if (outptr != NULL)
        {
            fwrite(block, 512, 1, outptr);
        }
    }
    // close the last image file if any
    if (outptr != NULL)
    {
        fclose(outptr);
    }
}
