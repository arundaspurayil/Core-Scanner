from Core import Core

class Scanner:
  # Initialize the scanner
  def __init__(self, filename):
    self.count = 0
    self.whiteSpaceCount = 0
    self.end = False
    file = open(filename,"r")

    self.tokens = list(file.read())
    #self.tokens = list(filter(lambda char: char != ' ' and char != '\t' and char != '\n', file.read()))

    file.close()

  # Advance to the next token
  def nextToken(self):
    self.count += self.whiteSpaceCount
    token = self.currentToken()

    if token == Core.ID:
      self.count += len(self.getID())
    elif token == Core.CONST:
      self.count += len(self.getCONST())
    elif token == Core.ASSIGN or token == Core.LESSEQUAL or token == Core.IF:
      self.count += 2
    elif token == Core.LESS or token == Core.SEMICOLON or token == Core.LPAREN or token == Core.RPAREN or token == Core.COMMA:
      self.count += 1
    elif token == Core.PROGRAM or token == Core.INT or token == Core.OUTPUT or token == Core.INPUT or token == Core.BEGIN or token==Core.WHILE or token == Core.ENDWHILE or token == Core.ENDFUNC or token == Core.THEN or token == Core.ELSE or token == Core.ENDIF:
      self.count += len(token.name)
    else:
      self.count += 1

    

    """
    if token == Core.PROGRAM or token == Core.INT or token == Core.OUTPUT or token == Core.INPUT or token == Core.BEGIN:
      self.count += len(token.name)
    elif token == Core.ID:
      self.count += len(self.getID())
    elif token == Core.CONST:
      self.count += len(self.getCONST())
    elif token == Core.ASSIGN:
      self.count +=2
    else:
      self.count += 1
    """


  def currentToken(self):
    #if self.end:
     # return Core.EOS
    
    self.whiteSpaceCount=0
    currentToken = self.tokens[self.count]
    index = self.count
    while index<len(self.tokens) and (currentToken == ' ' or currentToken == '\n' or currentToken == '\t'):
      self.whiteSpaceCount += 1
      index += 1     
      currentToken = self.tokens[index]
      
    if currentToken ==  ";":
      return Core.SEMICOLON
    elif currentToken == ",":
      return Core.COMMA
    elif currentToken == "!":
      #Ask if negation is !
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
    
    if currentToken == ':':
      #CHECK FOR INDEX OUT OF BOUNDS
      if self.tokens[index+1] == "=":
        return Core.ASSIGN
      else:
        print("ERROR: Missing '=' after ':'!")
        return Core.EOS

    if currentToken == '<':
      if self.tokens[index+1] == "=":
        return Core.LESSEQUAL
      else:
        return Core.LESS
      
    
    if currentToken.isalpha():
      currentStr = ""
      while index<len(self.tokens) and self.tokens[index].isalpha():
        currentStr += self.tokens[index]
        #print(currentStr)
        
        if not (any(x.isupper() for x in currentStr)):
          if (currentStr == "end"):
            isWhile = False
            isFunc = False
            isIf = False
            try:
              if self.tokens[index+1] == 'w':
                isWhile = self.tokens[index+1] == 'w'
                isWhile = self.tokens[index+2] == 'h' and isWhile
                isWhile = self.tokens[index+3] == 'i' and isWhile
                isWhile = self.tokens[index+4] == 'l' and isWhile
                isWhile = self.tokens[index+5] == 'e' and isWhile
              elif self.tokens[index+1] == 'f':
                isFunc = self.tokens[index+1] == 'f' 
                isFunc = self.tokens[index+2] == 'u' and isFunc
                isFunc = self.tokens[index+3] == 'n' and isFunc
                isFunc = self.tokens[index+4] == 'c' and isFunc
              elif self.tokens[index+1] == 'i':
                isIf = self.tokens[index+1] == 'i' 
                isIf = self.tokens[index+2] == 'f' and isIf

              if isWhile:
                return Core.ENDWHILE
              elif isFunc:
                return Core.ENDFUNC
              elif isIf:
                return Core.ENDIF
            except Exception as e:
              pass
          try:
            token = Core[currentStr.upper()]
            if token == Core.END:
              self.end = True
            return token
          except Exception as e:
            pass

        index += 1
      if self.end != True:
        return Core.ID
        
    if currentToken.isdigit() and int(currentToken) in range(1024):
      index = self.count + self.whiteSpaceCount
      currentConst =""
      while index<len(self.tokens) and self.tokens[index].isdigit():
        currentConst += self.tokens[index]
        index +=1
      if int(currentConst) not in range(1024):
        print("Error: "+ currentConst +" not in range 0-1023!")
        return Core.EOS
      return Core.CONST
    
    if self.end != True:
      print("ERROR: Token not apart of Core language!")
    return Core.EOS
 
  def getID(self):
    index = self.count + self.whiteSpaceCount
    currentStr = ""
    while index<len(self.tokens) and (self.tokens[index].isalpha() or self.tokens[index] in range(1,10)):
      currentStr += self.tokens[index]
      index += 1
    return currentStr
      

  def getCONST(self):
      index = self.count + self.whiteSpaceCount
      currentConst =""
      while index<len(self.tokens) and self.tokens[index].isdigit():
        currentConst += self.tokens[index]
        index +=1
      
      return currentConst

  def checkIfValidToken(self,currentStr):
    try:
      token = Core[currentStr.upper()]
      return True
    except Exception as e:
      return False
