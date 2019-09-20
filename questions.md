# Questions

## What's `stdint.h`?

`stdint.h` is a library that contains special integer types of a certain number of bytes.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

The point of using such types is to make sure that a variable could hold a certain value or to save memory.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

There is 1 byte in a `BYTE`, 4 bytes in a `DWORD`, 4 bytes in a `LONG`, and 2 bytes in a `WORD`.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The first two bytes of any BMP file must be `0x4d42`.

## What's the difference between `bfSize` and `biSize`?

`bfSize` is the size of the `BITMAPFILEHEADER`, and `biSize` is the size of the `BITMAPINFOHEADER`.

## What does it mean if `biHeight` is negative?

If `biheight` is negative, the BMP is a top-down DIB with the origin at the top left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

`biBitCount` specifies the BMP's color depth.

## Why might `fopen` return `NULL` in `copy.c`?

`fopen` might return `NULL` if the file does not exists and is not opened as write-only or if there is a permission error.

## Why is the third argument to `fread` always `1` in our code?

The third argument to `fread` is always `1` in our code because we are always reading 1 element.

## What value does `copy.c` assign to `padding` if `bi.biWidth` is `3`?

`copy.c` assigns `0` to `padding` if `bi.biWidth` is `3`.

## What does `fseek` do?

`fseek` changes the file pointer location.

## What is `SEEK_CUR`?

`SEEK_CUR` is the current file pointer position (used in `fseek`).
