// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "bmp.h"


void printFileHeader(BITMAPFILEHEADER *bf)
{
    printf("bfType: %x\nbfSize: %x\nbfReserved1: %x\nbfReserved2: %x\nbfOffBits: %x\n",
           bf->bfType, bf->bfSize, bf->bfReserved1, bf->bfReserved2, bf->bfOffBits);
}


void printInfoHeader(BITMAPINFOHEADER *bi)
{
    printf("biSize: %x\nbiWidth: %x\nbiHeight: %x\nbiPlanes: %x\nbiBitCount: %x\n"
           "biCompression: %x\nbiSizeImage: %x\nbiXPelsPerMeter: %x\nbiYPelsPerMeter: %x\nbiClrUsed: %x\nbiClrImportant: %x\n",
           bi->biSize, bi->biWidth, bi->biHeight, bi->biPlanes, bi->biBitCount,
           bi->biCompression, bi->biSizeImage, bi->biXPelsPerMeter, bi->biYPelsPerMeter, bi->biClrUsed, bi->biClrImportant);
}


int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize f infile outfile\n");
        return 1;
    }

    // remember filenames
    float f = atof(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    if (f <= 0 || f > 100)
    {
        fprintf(stderr, "f should be in range (0.0, 100].\n");
        return 1;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // print old headers
    printFileHeader(&bf);
    printInfoHeader(&bi);

    BITMAPFILEHEADER newbf = bf;
    BITMAPINFOHEADER newbi = bi;

    // calculate width and height
    newbi.biWidth = (int)(bi.biWidth * f);
    newbi.biHeight = (int)(bi.biHeight * f);

    // determine padding for scanlines
    int oldPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int newPadding = (4 - (newbi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    newbi.biSizeImage = (newbi.biWidth * sizeof(RGBTRIPLE) + newPadding) * abs(newbi.biHeight);
    newbf.bfSize = newbf.bfOffBits + newbi.biSizeImage;

    // write outfile's BITMAPFILEHEADER
    fwrite(&newbf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&newbi, sizeof(BITMAPINFOHEADER), 1, outptr);


    // pixel data from inFile.
    RGBTRIPLE *inPixels = (RGBTRIPLE *)malloc(sizeof(RGBTRIPLE) * bi.biWidth * abs(bi.biHeight));
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // read a scanline
        fread(inPixels + i * bi.biWidth, sizeof(RGBTRIPLE), bi.biWidth, inptr);
        // skip over padding in infile, if any
        fseek(inptr, oldPadding, SEEK_CUR);
    }

    // filling bytes for padding, 4 bytes max.
    const char *filling = "\0\0\0\0";

    // generate pixel data
    for (int i = 0, biHeight = abs(newbi.biHeight); i < biHeight; i++)
    {
        for (int j = 0; j < newbi.biWidth; j++)
        {
            // write pixel
            fwrite(&inPixels[(int)(i / f) * bi.biWidth + (int)(j / f)], sizeof(RGBTRIPLE), 1, outptr);
        }

        if (newPadding > 0)
        {
            fwrite(filling, 1, newPadding, outptr);
        }
    }

    // free up allocated memory.
    free(inPixels);

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
