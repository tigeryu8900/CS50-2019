// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "bmp.h"


void printFileHeader(BITMAPFILEHEADER* bf)
{
    printf("bfType: %x\nbfSize: %x\nbfReserved1: %x\nbfReserved2: %x\nbfOffBits: %x\n",
           bf->bfType, bf->bfSize, bf->bfReserved1, bf->bfReserved2, bf->bfOffBits);
}


void printInfoHeader(BITMAPINFOHEADER* bi)
{
    printf("biSize: %x\nbiWidth: %x\nbiHeight: %x\nbiPlanes: %x\nbiBitCount: %x\n"
           "biCompression: %x\nbiSizeImage: %x\nbiXPelsPerMeter: %x\nbiYPelsPerMeter: %x\nbiClrUsed: %x\nbiClrImportant: %x\n",
           bi->biSize, bi->biWidth, bi->biHeight, bi->biPlanes, bi->biBitCount,
           bi->biCompression, bi->biSizeImage, bi->biXPelsPerMeter, bi->biYPelsPerMeter, bi->biClrUsed, bi->biClrImportant);
}


int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4) {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    // remember filenames
    int n = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL) {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL) {
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
        bi.biBitCount != 24 || bi.biCompression != 0) {
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
    newbi.biWidth = bi.biWidth * n;
    newbi.biHeight = bi.biHeight * n;

    // determine padding for scanlines
    int oldPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int newPadding = (4 - (newbi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    newbi.biSizeImage = (newbi.biWidth * sizeof(RGBTRIPLE) + newPadding) * abs(newbi.biHeight);
    newbi.biSize = newbf.bfOffBits + newbi.biSizeImage;

    // write outfile's BITMAPFILEHEADER
    fwrite(&newbf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&newbi, sizeof(BITMAPINFOHEADER), 1, outptr);


    // one scanline from inFile.
    RGBTRIPLE *inScanLine = (RGBTRIPLE *)malloc(sizeof(RGBTRIPLE) * bi.biWidth);
    // 2d array, n scanlines to be written to outfile.
    RGBTRIPLE **outScanLines = (RGBTRIPLE **)malloc((sizeof(RGBTRIPLE*) + sizeof(RGBTRIPLE) * newbi.biWidth) * n);
    for (int i = 0; i < n; ++i) {
        // allocate memory for n scanlines to be written to outfile.
        outScanLines[i] = (RGBTRIPLE *)(outScanLines + n);
    }

    // filling bytes for padding, 4 bytes max.
    const char* filling = "\0\0\0\0";

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++) {
        // read one scanline from infile
        fread(inScanLine, sizeof(RGBTRIPLE), bi.biWidth, inptr);
        // iterate over pixels in inScanline
        for (int j = 0; j < bi.biWidth; j++) {
            // fill outScanLines with a 2-level loop.
            for (int out_i = 0; out_i < n; ++out_i) {
                for (int out_j = j * n; out_j < j * n + n; ++out_j) {
                    (outScanLines[out_i])[out_j] = inScanLine[j];
                }
            }
        }

        // write outScanLines to outfile.
        for (int out_i = 0; out_i < n; ++out_i) {
            fwrite(outScanLines[out_i], sizeof(RGBTRIPLE), newbi.biWidth, outptr);
            if (newPadding > 0) {
                fwrite(&filling, 1, newPadding, outptr);
            }
        }

        // skip over padding in infile, if any
        fseek(inptr, oldPadding, SEEK_CUR);
    }

    // free up allocated memory.
    free(inScanLine);
    free(outScanLines);

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
