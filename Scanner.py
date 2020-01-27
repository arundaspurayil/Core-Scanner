from Core import Core

class Scanner:
  # Initialize the scanner
  def __init__(self, filename):
    """
      I implemented this by reading the entire file and seperating it by each character into a list
    """

    #self.count represents the index in the array that is currently being looked at
    self.count = 0
    #self.whiteSpaceCount represents the number of whitespace characters encountered before a token

    self.whiteSpaceCount = 0
    #self.end is True when Core.END is found
    self.end = False

    #Opens the file, reads each character into an array and closes the file
    file = open(filename,"r")
    self.tokens = list(file.read())
    file.close()

  # Advance to the next token
  def nextToken(self):
    #Move to the next token by ignoring the indices of all the whitespace characters
    self.count += self.whiteSpaceCount

    token = self.currentToken()

    #Compare the token returned from currentToken() to all the possible token values to determine how much to increment self.count
    #For example if the token returned is a + then we can move onto the next token by incrementing self.count by 1
    #self.count is the index of the start of the current token

    #Essentially since the file is separated into each char, the amount self.count gets incremented by 
    #corresponds to the number of indices to add before the next character is reached
    if token == Core.ID:
      #Increment the current index by the length of the ID the user gave
      self.count += len(self.getID())
    elif token == Core.CONST:
      #Increment the current index by the length of the number the user gave
      self.count += len(self.getCONST())
    elif token == Core.ASSIGN or token == Core.LESSEQUAL or token == Core.IF:
      self.count += 2
    elif token == Core.LESS or token == Core.SUB or token == Core.ADD or token == Core.SEMICOLON or token == Core.LPAREN or token == Core.RPAREN or token == Core.COMMA:
      self.count += 1
    elif token == Core.PROGRAM or token == Core.INT or token == Core.OUTPUT or token == Core.INPUT or token == Core.BEGIN or token==Core.WHILE or token == Core.ENDWHILE or token == Core.ENDFUNC or token == Core.THEN or token == Core.ELSE or token == Core.ENDIF:
      self.count += len(token.name)
    else:
      if token == Core.END:
        self.count += 3
      else:
        self.count += 1

  
  def currentToken(self):

    #Set whiteSpaceCount to 0 because currentTokens gets called multiple times so I don't want the same value to get added multiple times
    self.whiteSpaceCount=0

    currentToken = self.tokens[self.count]
    index = self.count

    #Loops through all whitespace characters and ignores them
    while index<len(self.tokens)-1 and (currentToken == ' ' or currentToken == '\n' or currentToken == '\t'):
      self.whiteSpaceCount += 1
      index += 1     
    
    #The first character that is not whitespace
    currentToken = self.tokens[index]
      
    #The if else statement below are all the possible 1 character tokens
    #The corresponing token gets returned
    if currentToken ==  ";":
      return Core.SEMICOLON
    elif currentToken == ",":
      return Core.COMMA
    elif currentToken == "!":
      return Core.NEGATION
    elif currentToken == "=":
      return Core.EQUAL
    elif currentToken == "+":
      return Core.ADD
    elif currentToken == "-":
      return Core.SUB
    elif currentToken == "*":
      return Core.MULT
    elif currentToken == "(":
      return Core.LPAREN
    elif currentToken == ")":
      return Core.RPAREN
    
    #Checks for the assignment token
    if currentToken == ':':
      #If index is still in bounds and the next character after the : is an = then return the ASSIGN token. Else it is an error.
      if (index < len(self.tokens)-1) and self.tokens[index+1] == "=":
        return Core.ASSIGN
      else:
        print("ERROR: Missing '=' after ':'!")
        return Core.EOS

    #If the current token is an < then check to see if the next token is an =
    if currentToken == '<':
      if (index < len(self.tokens)-1) and self.tokens[index+1] == "=":
        return Core.LESSEQUAL
      else:
        return Core.LESS
      
    #If the current token is a character in the alphabet then we want to look at the corresponding characters
    # and determine if it is a token in the core language or an ID
    currentStr = ""    
    if currentToken.isalpha():
      #While the current index is within bounds and the current token is an alphabetic character
      while index<len(self.tokens) and self.tokens[index].isalpha():
        #currentStr is the current token + the corresponding characters after it
        currentStr += self.tokens[index]
        
        #If statement is only true if all characters in currentStr are lowercase
        if not (any(x.isupper() for x in currentStr)):
          #If currentStr is "end" then we have to check if it is ENDWHILE ENDFUNC or ENDIF
          if (currentStr == "end"):
            isWhile = False
            isFunc = False
            isIf = False
            #Try catch statement is there to catch index out of bounds error and ignore it
            try:
              #Check if the next 5 characters are "while"
              if self.tokens[index+1] == 'w':
                isWhile = self.tokens[index+1] == 'w'
                isWhile = self.tokens[index+2] == 'h' and isWhile
                isWhile = self.tokens[index+3] == 'i' and isWhile
                isWhile = self.tokens[index+4] == 'l' and isWhile
                isWhile = self.tokens[index+5] == 'e' and isWhile
              #Check if the next 4 characters are "func"
              elif self.tokens[index+1] == 'f':
                isFunc = self.tokens[index+1] == 'f' 
                isFunc = self.tokens[index+2] == 'u' and isFunc
                isFunc = self.tokens[index+3] == 'n' and isFunc
                isFunc = self.tokens[index+4] == 'c' and isFunc
              #Check if it is an ENDIF
              elif self.tokens[index+1] == 'i':
                isIf = self.tokens[index+1] == 'i' 
                isIf = self.tokens[index+2] == 'f' and isIf
              
              #If it is ENDFUNC, ENDWHILE or ENDIF return the corresponding token
              if isWhile:
                return Core.ENDWHILE
              elif isFunc:
                return Core.ENDFUNC
              elif isIf:
                return Core.ENDIF
            except Exception as e:
              pass
          
          """
            The try catch statement takes each currentStr and determines if it is in the core language
            Try catch is there because if the currentStr isn't in the Core language then it returns an error
          """
          try:
            #Check if token is in the core language
            token = Core[currentStr.upper()]
            #If the token returned is Core.END then the program is over thus self.end is true and the token gets returned
            if token == Core.END:
              self.end = True
            return token
          except Exception as e:
            pass

        #Look at the next character in the list
        index += 1
      
      #At this point currentStr is not apart of the Core language thus it is an ID
      if self.end != True:
        return Core.ID
        
    #If the current token is a digit and it is not a leading 0 then if statement is true
    if currentToken.isdigit() and int(currentToken) != 0:
      #Look at the current index of self.tokens
      index = self.count + self.whiteSpaceCount
      currentConst =""
      #Add the current digit to currentConst and look at the characters after it to determine if it is a part of the number
      while index<len(self.tokens) and self.tokens[index].isdigit():
        currentConst += self.tokens[index]
        index +=1
      #Make sure the digit is in range
      if int(currentConst) not in range(1024):
        print("Error: "+ currentConst +" not in range 0-1023!")
        return Core.EOS
      return Core.CONST
    else:
      print("Error: Can't have leading 0!")
      return Core.EOS
    
    #If there is any text after the END statement
    if self.end and index != len(self.tokens)-1:
        print("ERROR: No text allowed after END keyword!")
    #If there hasn't been an END statement yet and the program makes it to this line then
    #The token is invalid and not apart of the language thus it throws an error
    elif not self.end:
      print("Error: Invalid token!")

    return Core.EOS
    
 
  def getID(self):
    #Index is the current index of self.tokens to look at
    index = self.count + self.whiteSpaceCount
    #CurrentStr is the ID that will be returned
    currentStr = ""
    #While index is in bounds and the current token is an alphabetic character or a digit in the range 1-9
    while index<len(self.tokens) and (self.tokens[index].isalpha() or self.tokens[index] in range(1,10)):
      #Add the current token to currentStr
      currentStr += self.tokens[index]
      index += 1
    return currentStr
      

  def getCONST(self):
    #Index is the current index of self.tokens to look at
    index = self.count + self.whiteSpaceCount
    #currentConst is the CONST that will ber eturned
    currentConst =""
    #While index is in range and the current token is a digit, add the digit to currentConst and return it
    while index<len(self.tokens) and self.tokens[index].isdigit():
      currentConst += self.tokens[index]
      index +=1
    
    return currentConst

  #Check if needed
  def checkIfValidToken(self,currentStr):
    try:
      token = Core[currentStr.upper()]
      return True
    except Exception as e:
      return False
