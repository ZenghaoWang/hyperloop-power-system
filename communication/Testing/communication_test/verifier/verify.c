/*
  verify.c

  Simple tool used to verify if the given output, given by the CANBUS, had any
  errors in it.

  Usage:
  ./a.out <filepath>

  Where filepath is a file containing the data transmitted over the CANBUS.

  Alexandre Singer
  February 2023
*/

#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
  if (argc != 2) {
    printf("Invalid number of arguments.\n");
    return -1;
  }

  FILE *fptr = fopen(argv[1], "r");
  if (fptr == NULL) {
    printf("Unable to open file: %s\n", argv[1]);
    return -1;
  }

  printf("Verifying the file...\n");

  char prev_char = fgetc(fptr);
  if (prev_char == EOF) {
    printf("Cannot verify empty file.\n");
    return -1;
  }

  size_t count = 0;
  size_t num_errors = 0;
  char c;

  // Simple loop to check that the input file is a sequence of capital letters
  // in alphabetical order wrapping from Z back to A.
  while ((c = fgetc(fptr)) != EOF) {
    char expected_char = (((prev_char - 65) + 1) % 26) + 65;
    if (c != expected_char) {
      printf("Error in string at position %lu!\n", count);
      num_errors++;
    }
    prev_char = c;
    count++;
  }

  printf("Found %lu errors in %lu characters.\n", num_errors, count);
}