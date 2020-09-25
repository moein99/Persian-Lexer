import os

from codeTranslator import CodeTranslator
from Lexer import Lexer
import pickle

print("Enter the source code address : ")
fileAddress = input()
print("Enter destination file name : ")
destinationFileName = input()
print("Enter destination language : (fa/en)")
type = input()

sourceCodeAddress = fileAddress.split('\\')[-1]
sourceCodeAddress = fileAddress.split(sourceCodeAddress)[0]

types = ['fa', 'en']
assert type in types

if type == 'fa':
    lexer = Lexer(fileAddress, 'en')
else:
    lexer = Lexer(fileAddress, 'fa')

token = lexer.getNextToken()
CodeTranslator = CodeTranslator()
f = open(sourceCodeAddress + destinationFileName, "w", encoding="utf-8")
toBeWritten = ""
row = 0
col = 0
translated = ''

objectName = fileAddress.split('.txt')[0].split('\\')[-1]
object = None
flag = True
if os.path.isfile(sourceCodeAddress + objectName + type):
    with open(sourceCodeAddress + objectName + type, 'rb') as config_dictionary_file:
        object = pickle.load(config_dictionary_file)
if object is None:
    object = {}
    flag = False

while token is not None:
    toBeWritten = ""
    if row != token.row:
        toBeWritten += "\n" * (token.row - row)
        toBeWritten += ' ' * (token.column - 1)
        row = token.row
    if flag:
        translated = object[token.content]
    else:
        if type == 'fa':
            translated = CodeTranslator.toPer(token.content, token.type)
        else:
            translated = CodeTranslator.toEng(token.content, token.type)
        object[translated] = token.content
    if token.type == "STRING_LITERAL":
        translated = '\"' + translated + '\"'
    toBeWritten += translated + " "
    f.write(toBeWritten)
    token = lexer.getNextToken()

if not flag:
    name = ""
    for i in types:
        if i != type:
            name = i
            break
    with open(sourceCodeAddress + destinationFileName.split('.txt')[0] + name, 'wb') as dictionary_file:
        pickle.dump(object, dictionary_file)
f.close()