# COMPILER PYTHON

# recognize \n from reading file

from node import Node, BinOp, UnOp, IntVal, NoOp, Print, Assignment, Statement, Identifier
from pre_process import PrePro
from symboltable import SymbolTable
from string import ascii_letters, ascii_lowercase
import sys

CHAR = {
    "+" : "PLUS",
    "-" : "MINUS",
    "*" : "MULT",
    "/" : "DIV",
    "(" : "OPENP",
    ")" : "CLOSEP",
    "=" : "EQUAL"
}

DOUBLE_CHAR = {
    "\\n" : "BREAK_LINE"
}

RESERVED = ['print','begin','end']

VARNAME_CHARS = '0123456789_' + ascii_letters

class Token():

    def __init__(self, tp, value):
        self.tp = tp
        self.value = value

class Tokenizer():

    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self): 

        # Tokenize the expression
        if self.position < len(self.origin):

            # ignore spaces
            while self.origin[self.position] == " ":
                self.position += 1
                if self.position == len(self.origin):
                    break   
            
            if self.origin[self.position].isdigit():
                
                num = ""
    
                while self.origin[self.position].isdigit():

                    num += self.origin[self.position]
                    self.position += 1

                    if self.position  == len(self.origin):
                        break
                    
                token = Token("INT",int(num))

            elif self.origin[self.position] in CHAR:

                token = Token(CHAR[self.origin[self.position]],self.origin[self.position])
                self.position += 1
            
            elif self.origin[self.position] == "\n":
                token = Token("BREAK_LINE","\\n")
                self.position += 1

            elif self.origin[self.position].isalpha():
                if self.origin[self.position].islower():
                    
                    aux = ""

                    while self.origin[self.position] in VARNAME_CHARS:

                        aux += self.origin[self.position]
                        self.position += 1
                       
                        if self.position  == len(self.origin):
                            break

                    if aux in RESERVED:
                        token = Token(aux.upper(),aux)

                    else:
                        token = Token("IDENTIFIER", aux)

                else:
                    raise SyntaxError("First letter must be lowercase")


            else:

                # Invalid Token
                raise ValueError(f"{self.origin[self.position]} is not a number")   

        # End of File 
        else:

            token = Token("EOF", None)

        self.actual = token

        #print(self.actual.tp,self.actual.value)


class Parser():

    tokens = None

    def run(source):

        source = PrePro.filter(source)
        Parser.tokens = Tokenizer(source)
        Parser.tokens.selectNext()

        st = SymbolTable()

        Parser.parseStatements().Evaluate(st)
        
        if Parser.tokens.actual.tp != "EOF":
            raise ValueError(f"{Parser.tokens.actual.value} invalid at end of sentence")

    def parseFactor():

        Parser.tokens.selectNext()

        if Parser.tokens.actual.tp == "INT":
            node = IntVal(Parser.tokens.actual.value)
            #result = int(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.tp == "PLUS":
            node = UnOp("+",Parser.parseFactor())
            #result = Parser.parseFactor()

        elif Parser.tokens.actual.tp == "MINUS":
            #result = - Parser.parseFactor()
            node = UnOp("-",Parser.parseFactor())

        elif Parser.tokens.actual.tp == "OPENP":
            node = Parser.parseExpression()

            if Parser.tokens.actual.tp != "CLOSEP":
                raise ValueError("Missing parentheses")
            else:
                Parser.tokens.selectNext()
        
        elif Parser.tokens.actual.tp == "IDENTIFIER":
            node = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
        else:
            raise ValueError(f"{Parser.tokens.actual.value} not a valid operator")

        return node


    def parseTerm():

        node = Parser.parseFactor()

        while Parser.tokens.actual.tp == "DIV" or  Parser.tokens.actual.tp == "MULT":

            if Parser.tokens.actual.tp == "MULT":
                #result *= Parser.parseFactor()
                node = BinOp("*",[node,Parser.parseFactor()])

            elif Parser.tokens.actual.tp == "DIV":
                #result //= Parser.parseFactor()
                node = BinOp("/",[node,Parser.parseFactor()])

        return node


    def parseExpression():

        node = Parser.parseTerm()

        while Parser.tokens.actual.tp == "PLUS" or  Parser.tokens.actual.tp == "MINUS":

            if Parser.tokens.actual.tp == "PLUS":
                #result += Parser.parseTerm()
                node = BinOp("+",[node,Parser.parseTerm()])

            elif Parser.tokens.actual.tp == "MINUS":
                #result -= Parser.parseTerm()
                node = BinOp("-",[node,Parser.parseTerm()])

        return node

    def parseStatement():


        if Parser.tokens.actual.tp == "IDENTIFIER":
            variable_name = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            if Parser.tokens.actual.tp == "EQUAL":
                node = Assignment([variable_name, Parser.parseExpression()])
        
        elif Parser.tokens.actual.tp == "PRINT":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.tp == "OPENP":
                node = Print(Parser.parseExpression())

                if Parser.tokens.actual.tp != "CLOSEP":
                    raise SyntaxError("Missing parentheses")
                Parser.tokens.selectNext()

        elif Parser.tokens.actual.tp == "BEGIN":
            node = Parser.parseStatements()
               
        return node 

    def parseStatements():

        statements_children = []

        if  Parser.tokens.actual.tp == "BEGIN":
            Parser.tokens.selectNext()

            if Parser.tokens.actual.tp == "BREAK_LINE":
                Parser.tokens.selectNext()

                while Parser.tokens.actual.tp != "END":
                    
                    statements_children.append(Parser.parseStatement())
                    
                    while(Parser.tokens.actual.tp == "BREAK_LINE"):
                        Parser.tokens.selectNext()

                node = Statement(statements_children)
                Parser.tokens.selectNext()

                return node
            
            else:
                raise SyntaxError("END statement missing")
        
        else:
            raise SyntaxError("BEGIN statement missing")

with open(sys.argv[1], 'r') as myfile:
    source = myfile.read()
#print(source)

Parser.run(source)