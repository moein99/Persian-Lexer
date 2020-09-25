from translator import Translate

class CodeTranslator:
    def __init__(self):
        self.engToPerDic = {"False" : "غلط", "None" : "هیچی", "True" : "درست", "and" : "و", "as" : "بعنوان", "assert" : "تاکید", "break" : "خارج", "class" : "کلاس", "continue" : "ادامه", "def" : "تعریف", "del" : "حذف", "elif" : "شرط_دیگر", "else" : "درغیراینصورت", "except" : "بجز", "finally" : "دراخر", "for" : "برای", "from" : "از", "global" : "جهانی", "if" : "اگر", "import" : "واردکن", "in" : "داخل", "is" : "هست", "lambda" : "لاندا", "nonlocal" : "غیرمحلی", "not" : "نفی", "or" : "یا", "pass" : "بگذر", "raise" : "زیادکن", "return" : "برگردان", "try" : "ازمون", "while" : "تازمانیکه", "with" : "با", "yield" : "واگذارکن", "self" : "خود", "print" : "چاپ"}
        self.perToEndDic = {"غلط" : "False", "هیچی" : "None", "درست" : "True", "و" : "and", "بعنوان" : "as", "تاکید" : "assert", "خارج" : "break", "کلاس" : "class", "ادامه" : "continue", "تعریف" : "def", "حذف" : "del", "شرط_دیگر" : "elif", "درغیراینصورت" : "else", "بجز" : "except", "دراخر" : "finally", "برای" : "for", "از" : "from", "جهانی" : "global", "اگر" : "if", "واردکن" : "import", "داخل" : "in", "هست" : "is", "لاندا" : "lambda", "غیرمحلی" : "nonlocal", "نفی" : "not", "یا" : "or", "بگذر" : "pass", "زیادکن" : "raise", "برگردان" : "return", "ازمون" : "try", "تازمانیکه" : "while", "با" : "with", "واگذارکن" : "yield", "خود" : "self", "چاپ" : "print"}
        self.translator = Translate()
    def toPer(self, word, type):
        if (type == "KEYWORD" or type == "IDENTIFIER"):
            if word in  self.engToPerDic:
                return self.engToPerDic[word]
            else:
                return self.translator.translateToPersian(word)
        else:
            return word
    def toEng(self, word, type):
        if (type == "KEYWORD" or type == "IDENTIFIER"):
            if word in self.perToEndDic:
                return self.perToEndDic[word]
            else:
                return self.translator.translateToEng(word)
        else:
            return word