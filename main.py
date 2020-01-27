import sys
from Scanner import Scanner
from Core import Core

# Run using the command "python3 main.py FILENAME"
def main(argv):
  # Initialize the scanner with the input file
  S = Scanner(argv[0])

  while (S.currentToken() != Core.EOS):
    # Print the current token, with any extra data needed
    print(S.currentToken().name, end='')
    if (S.currentToken() == Core.ID):
      value = S.getID()
      print("[" + value + "]", end='');
    elif (S.currentToken() == Core.CONST):
      value = S.getCONST()
      print("[" + str(value) + "]", end='');
    print();
    # Advance to the next token
    S.nextToken();


if __name__ == "__main__":
    main(sys.argv[1:])
