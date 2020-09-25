class Lexer:
    def __init__(self, fileAddress, type):
        self.file = open(fileAddress, 'r', encoding="utf-8")
        self.state = 0
        self.lastcharacter = '\0'
        self.row = 0
        self.column = 0
        self.curTokenType = None
        self.compileLanguage = type
        self.engKeyWords = ["False", "None", "True", "and", "as", "assert", "break", "class", "continue", "def", "del",
                            "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is",
                            "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with",
                            "yield"]
        self.perKeyWords = ["تعریف", "واردکن", "ادامه", "واگذارکن", "بگذر", "با", "شرط_دیگر", "ازمون", "لاندا",
                            "برگردان", "جهانی", "داخل", "بعنوان", "برای", "هست", "دراخر", "حذف", "هیچی", "غیرمحلی",
                            "چاپ", "تاکید", "زیادکن", "نفی", "خارج", "از", "درست", "غلط", "خود", "و", "بجز", "یا",
                            "اگر", "درغیراینصورت", "کلاس", "تازمانیکه"]

        if self.compileLanguage == 'fa':
            self.keyWords = self.perKeyWords
        else:
            self.keyWords = self.engKeyWords
        self.TokenType = TokenType()
        self.perAlphabet = "اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
        self.lastIteration = True

    def isLetter(self, c):
        if c == '':
            return False
        if (self.compileLanguage == 'fa'):
            return c in self.perAlphabet
        else:
            asc = ord(c)
            if (65 <= asc <= 90) or (97 <= asc <= 122):
                return True
        return False

    def isDigit(self, c):
        if c == '':
            return False
        asc = ord(c)
        return 48 <= asc <= 57

    def getNextToken(self):
        nextWord = ""
        tokenType = ""
        quotationType = ''
        quotationRepCount = 0
        c = '\0'
        if self.lastcharacter != '\0':
            c = self.lastcharacter
            self.lastcharacter = '\0'
        else:
            c = self.file.read(1)
        while c != '' or self.lastIteration:
            if c == '' and self.lastIteration == True:
                self.lastIteration = False
            if self.state == 0:
                if c == '\t':
                    self.column += 4
                elif c == '\n':
                    self.row += 1
                    self.column = 0
                elif c == ' ':
                    self.column += 1
                elif self.isLetter(c):
                    nextWord += c
                    self.state = 1
                    self.column += 1
                elif self.isDigit(c):
                    nextWord += c
                    self.column += 1
                    self.state = 2
                elif c == ':':
                    self.column += 1
                    return Token(":", self.TokenType.COLON, self.row, self.column)
                elif c == '=':
                    self.column += 1
                    self.state = 17
                elif c == '#':
                    self.state = 4
                elif c == '\'' or c == '\"':
                    quotationType = c
                    self.column += 1
                    self.state = 5
                elif c == ',':
                    self.column += 1
                    return Token(",", self.TokenType.COMMA, self.row, self.column)
                elif c == ';':
                    self.column += 1
                    return Token(";", self.TokenType.SEMICOLON, self.row, self.column)
                elif c == '(':
                    self.column += 1
                    return Token("(", self.TokenType.O_PARENTHESE, self.row, self.column)
                elif c == ')':
                    self.column += 1
                    return Token(")", self.TokenType.C_PARENTHESE, self.row, self.column)
                elif c == '[':
                    self.column += 1
                    return Token("[", self.TokenType.O_sBRACKET, self.row, self.column)
                elif c == ']':
                    self.column += 1
                    return Token("]", self.TokenType.C_sBRACKET, self.row, self.column)
                elif c == '{':
                    self.column += 1
                    return Token("{", self.TokenType.O_cBRACKET, self.row, self.column)
                elif c == '}':
                    self.column += 1
                    return Token("}", self.TokenType.C_cBRACKET, self.row, self.column)
                elif c == '.':
                    self.column += 1
                    return Token(".", self.TokenType.DOT, self.row, self.column)
                elif c == '+':
                    self.column += 1
                    self.state = 10
                elif c == '-':
                    self.column += 1
                    self.state = 11
                elif c == '%':
                    self.column += 1
                    self.state = 12
                elif c == '*':
                    self.column += 1
                    self.state = 13
                elif c == '/':
                    self.column += 1
                    self.state = 14
                elif c == '>':
                    self.column += 1
                    self.state = 15
                elif c == '<':
                    self.column += 1
                    self.state = 16
                elif c == '!':
                    self.column += 1
                    self.state = 18
                elif c == '&':
                    self.column += 1
                    return Token("&", self.TokenType.BINARY_AND, self.row, self.column)
                elif c == '|':
                    self.column += 1
                    return Token("|", self.TokenType.BINARY_OR, self.row, self.column)
                elif c == '^':
                    self.column += 1
                    return Token("^", self.TokenType.BINARY_XOR, self.row, self.column)
            elif self.state == 1:
                self.column += 1
                if not (self.isLetter(c) or self.isDigit(c) or c == '_'):
                    if c == '$' or c == '@' or c == '!':
                        nextWord += c
                        self.state = 0
                        return Token(nextWord, self.TokenType.ERR_BAD_CHAR, self.row, self.column - len(nextWord))
                    self.lastcharacter = c
                    if nextWord in self.keyWords:
                        tokenType = self.TokenType.KEYWORD
                    else:
                        tokenType = self.TokenType.IDENTIFIER
                    self.state = 0
                    return Token(nextWord, tokenType, self.row, self.column - len(nextWord))
                nextWord += c
            elif self.state == 2:
                self.column += 1
                if not self.isDigit(c):
                    if c == '.':
                        self.state = 3
                        nextWord += c
                    else:
                        self.lastcharacter = c
                        self.state = 0
                        return Token(nextWord, self.TokenType.NUMBER, self.row, self.column - len(nextWord))
                nextWord += c
            elif self.state == 3:
                self.column += 1
                if not self.isDigit(c):
                    self.lastcharacter = c
                    self.state = 0
                    return Token(nextWord, self.TokenType.REAL_NUMBER, self.row, self.column - len(nextWord))
                nextWord += c
            elif self.state == 4:
                if c == '\n':
                    self.row += 1
                    self.state = 0
            elif self.state == 5:
                self.column += 1
                if c == '\\':
                    nextWord += c
                    self.state = 6
                if c == quotationType:
                    if len(nextWord) == 0:
                        self.state = 7
                    else:
                        self.state = 0
                        return Token(nextWord, self.TokenType.STRING_LITERAL, self.row, self.column - len(nextWord))
                nextWord += c
            elif self.state == 6:
                self.column += 1
                nextWord += c
                self.state = 5
            elif self.state == 7:
                self.column += 1
                if c == quotationType:
                    self.state = 8
                else:
                    self.lastcharacter = c
                    self.state = 0
                    return Token(nextWord, self.TokenType.STRING_LITERAL, self.row, self.column)
            elif self.state == 8:
                self.column += 1
                if c == quotationType:
                    self.state = 9
                if c == '':
                    self.state = 0
                    return Token(nextWord, self.TokenType.ERR_NOT_CLOSED_STRING, self.row, self.column)
                if c == '\n':
                    self.row += 1
                    self.column = 0
                nextWord += c
            elif self.state == 9:
                self.column += 1
                if c == quotationType:
                    if quotationRepCount == 0:
                        quotationRepCount += 1
                    else:
                        self.state = 0
                        return Token(nextWord, self.TokenType.STRING_LITERAL, self.row, self.column)
                else:
                    for i in range(quotationRepCount):
                        nextWord += quotationType
                    nextWord += c
                    self.state = 0
                    return Token(nextWord, self.TokenType.ERR_NOT_CLOSED_STRING, self.row, self.column)
            elif self.state == 10:
                self.column += 1
                self.state = 0
                if c == '=':
                    return Token("+=", self.TokenType.ADD_EQUAL_OPERATOR, self.row, self.column)
                else:
                    self.lastcharacter = c
                    return Token("+", self.TokenType.ADD_OPERATOR, self.row, self.column)
            elif self.state == 11:
                self.column += 1
                self.state = 0
                if c == '=':
                    return Token("-=", self.TokenType.SUBTRACT_EQUAL_OPERATOR, self.row, self.column)
                else:
                    self.lastcharacter = c
                    return Token("-", self.TokenType.SUBTRACT_OPERATOR, self.row, self.column)
            elif self.state == 12:
                self.column += 1
                self.state = 0
                if c == '=':
                    return Token("%=", self.TokenType.MODULUS_EQUAL_OPERATOR, self.row, self.column)
                else:
                    self.lastcharacter = c
                    return Token("%", self.TokenType.MODULUS_OPERATOR, self.row, self.column)
            elif self.state == 13:
                self.column += 1
                self.state = 0
                if c == '=':
                    return Token("*=", self.TokenType.MULTIPLY_EQUAL_OPERATOR, self.row, self.column)
                elif c == '*':
                    self.state = 19
                else:
                    self.lastcharacter = c
                    return Token("*", self.TokenType.MULTIPLY_OPERATOR, self.row, self.column)
            elif self.state == 14:
                self.column += 1
                self.state = 0
                if c == '=':
                    return Token("/=", self.TokenType.DIVIDE_EQUAL_OPERATOR, self.row, self.column)
                elif c == '/':
                    return Token("//", self.TokenType.FLOOR_DIVISION, self.row, self.column)
                else:
                    self.lastcharacter = c
                    return Token("/", self.TokenType.DIVIDE_OPERATOR, self.row, self.column)
            elif self.state == 15:
                self.column += 1
                self.state = 0
                if c == '=':
                    return Token(">=", self.TokenType.LARGER_THAN_EQUAL, self.row, self.column)
                elif c == '>':
                    return Token(">>", self.TokenType.SHIFT_RIGHT, self.row, self.column)
                else:
                    self.lastcharacter = c
                    return Token(">", self.TokenType.LARGER_THAN, self.row, self.column)
            elif self.state == 16:
                self.column += 1
                self.state = 0
                if c == '=':
                    return Token("<=", self.TokenType.SMALLER_THAN_EQUAL, self.row, self.column)
                elif c == '<':
                    return Token("<<", self.TokenType.SHIFT_LEFT, self.row, self.column)
                else:
                    self.lastcharacter = c
                    return Token("<", self.TokenType.SMALLER_THAN, self.row, self.column)
            elif self.state == 17:
                self.column += 1
                self.state = 0
                if c == '=':
                    return Token("==", self.TokenType.EQUAL_TO, self.row, self.column - 1)
                else:
                    self.lastcharacter = c
                    return Token("=", self.TokenType.ASSIGNMENT, self.row, self.column - 1)
            elif self.state == 18:
                self.column += 1
                self.state = 0
                if c == '=':
                    return Token("!=", self.TokenType.NOT_EQUAL, self.row, self.column)
                else:
                    self.lastcharacter = c
                    return Token("!", self.TokenType.NOT, self.row, self.column)
            elif self.state == 19:
                self.column += 1
                self.state = 0
                if c == '=':
                    return Token("**=", self.TokenType.EXPONENT_EQUAL, self.row, self.column)
                else:
                    self.lastcharacter = c
                    return Token("**", self.TokenType.EXPONENT, self.row, self.column)
            c = self.file.read(1)
        return None


class Token:
    def __init__(self, content, type, row, column):
        self.content = content
        self.type = type
        self.row = row
        self.column = column

    def getContent(self):
        return self.content

    def getType(self):
        return self.type

    def getRow(self):
        return self.row

    def getColumn(self):
        return self.column


class TokenType:
    def __init__(self):
        self.NUMBER = "NUMBER"
        self.REAL_NUMBER = "REAL_NUMBER"
        self.ADD_OPERATOR = "ADD_OPERATOR"
        self.SUBTRACT_OPERATOR = "SUBTRACT_OPERATOR"
        self.MULTIPLY_OPERATOR = "MULTIPLY_OPERATOR"
        self.MULTIPLY_EQUAL_OPERATOR = "MULTIPLY_EQUAL_OPERATOR"
        self.DIVIDE_OPERATOR = "DIVIDE_OPERATOR"
        self.DIVIDE_EQUAL_OPERATOR = "DIVIDE_EQUAL_OPERATOR"
        self.STRING_LITERAL = "STRING_LITERAL"
        self.MODULUS_OPERATOR = "MODULUS_OPERATOR"
        self.MODULUS_EQUAL_OPERATOR = "MODULUS_EQUAL_OPERATOR"
        self.ADD_EQUAL_OPERATOR = "ADD_EQUAL_OPERATOR"
        self.SUBTRACT_EQUAL_OPERATOR = "SUBTRACT_EQUAL_OPERATOR"
        self.COLON = "COLON"
        self.NOT = "NOT"
        self.NOT_EQUAL = "NOT_EQUAL"
        self.COMMA = "COMMA"
        self.ASSIGNMENT = "ASSIGNMENT"
        self.SEMICOLON = "SEMICOLON"
        self.EQUAL_TO = "EQUAL_TO"
        self.EXPONENT = "EXPONENT"
        self.EXPONENT_EQUAL = "EXPONENT_EQUAL"
        self.SMALLER_THAN = "SMALLER_THAN"
        self.SMALLER_THAN_EQUAL = "SMALLER_THAN_EQUAL"
        self.LARGER_THAN = "LARGER_THAN"
        self.LARGER_THAN_EQUAL = "LARGER_THAN_EQUAL"
        self.IDENTIFIER = "IDENTIFIER"
        self.KEYWORD = "KEYWORD"
        self.BINARY_AND = "BINARY_AND"
        self.BINARY_OR = "BINARY_OR"
        self.BINARY_XOR = "BINARY_XOR"
        self.SHIFT_LEFT = "SHIFT_LEFT"
        self.SHIFT_RIGHT = "SHIFT_RIGHT"
        self.O_PARENTHESE = "O_PARENTHESE"
        self.C_PARENTHESE = "C_PARENTHESE"
        self.FLOOR_DIVISION = "FLOOR_DIVISION"
        self.ERR_BAD_CHAR = "ERR_BAD_CHAR"
        self.ERR_NOT_CLOSED_STRING = "ERR_NOT_CLOSED_STRING"
        self.DOT = "DOT"
        self.O_sBRACKET = "["
        self.C_sBRACKET = "]"
        self.O_cBRACKET = "{"
        self.C_cBRACKET = "}"
