# COMPILER PYTHON

# update parser
# mydict.keys()[mydict.values().index(value)]

# v2.3

from node import Node, BinOp, UnOp, IntVal, NoOp, Print, Assignment, Identifier, Input, While, If, VarDec, Type, BoolVal, Program
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
    "=" : "EQUAL",
    "<" : "LESS_THAN",
    ">" : "GREATER_THAN"

}

RESERVED = ['print','begin','end','and','or','not','while','wend','if','then','else','dim','true','false','sub','as','boolean','integer','main']

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

        eof = True

        # Tokenize the expression
        if self.position < len(self.origin): 
            eof = False

        # ignore spaces
        if not eof:
            while self.origin[self.position] == " ":
                self.position += 1
                if self.position == len(self.origin):
                    eof = True
                    break  
            
        if not eof:
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

                # Invalid Token
                raise ValueError(f"{self.origin[self.position]} is not a number")   

        # End of File 
        else:

            token = Token("EOF", None)

        self.actual = token

        print(self.actual.tp,self.actual.value)


class Parser():

    tokens = None

    @staticmethod
    def run(source):

        source = PrePro.filter(source)
        Parser.tokens = Tokenizer(source)
        Parser.tokens.selectNext()

        st = SymbolTable()

        # WRITE ASSEMBLY HEADER
        file = open("source_code.asm", "w+", encoding="utf-8")    
        with open("header.asm", "r", encoding="utf-8") as header:
            for line in header.readlines():
              file.write(line)

        file.close()

        Parser.program().Evaluate(st)
        
        file = open("source_code.asm", "a", encoding="utf-8")    
        with open("footer.asm", "r", encoding="utf-8") as footer:
            for line in footer.readlines():
              file.write(line)

        if Parser.tokens.actual.tp != "EOF":
            raise ValueError(f"{Parser.tokens.actual.value} invalid at end of sentence")

    def parseFactor():



        #Parser.tokens.selectNext()

        if Parser.tokens.actual.tp == "INT":
            node = IntVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.tp == "PLUS":
            node = UnOp("+",Parser.parseFactor())

        elif Parser.tokens.actual.tp == "MINUS":
            node = UnOp("-",Parser.parseFactor())
        
        elif Parser.tokens.actual.tp == "NOT":
            node = UnOp("NOT",Parser.parseFactor())

        elif Parser.tokens.actual.tp in ["TRUE","FALSE"]:
            node = BoolVal(Parser.tokens.actual.tp)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.tp == "OPENP":
            Parser.tokens.selectNext()
            node = Parser.parseExpression()

            if Parser.tokens.actual.tp != "CLOSEP":
                raise ValueError("Missing parentheses")
            else:
                Parser.tokens.selectNext()
        
        elif Parser.tokens.actual.tp == "IDENTIFIER":
            node = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.tp == "INPUT":
            node = Input()
            Parser.tokens.selectNext()

        else:
            raise ValueError(f"{Parser.tokens.actual.value} not a valid operator")

        return node


    def parseTerm():

        node = Parser.parseFactor()

        while Parser.tokens.actual.tp in ["DIV","MULT","AND"]:

            if Parser.tokens.actual.tp == "MULT":
                Parser.tokens.selectNext()
                node = BinOp("*",[node,Parser.parseFactor()])

            elif Parser.tokens.actual.tp == "DIV":
                Parser.tokens.selectNext()
                node = BinOp("/",[node,Parser.parseFactor()])

            elif Parser.tokens.actual.tp == "AND":
                Parser.tokens.selectNext()
                node = BinOp("AND",[node,Parser.parseFactor()])

        return node


    def parseExpression():

        node = Parser.parseTerm()

        while Parser.tokens.actual.tp in ["PLUS","MINUS","OR"]:

            if Parser.tokens.actual.tp == "PLUS":
                node = BinOp("+",[node,Parser.parseTerm()])

            elif Parser.tokens.actual.tp == "MINUS":
                node = BinOp("-",[node,Parser.parseTerm()])

            elif Parser.tokens.actual.tp == "OR":
                node = BinOp("OR",[node,Parser.parseTerm()])

        return node

    def parseRelExpression():

        node = Parser.parseExpression()

        if Parser.tokens.actual.tp in ["EQUAL","GREATER_THAN","LESS_THAN"]:

            if Parser.tokens.actual.tp == "EQUAL":
                node = BinOp("=",[node,Parser.parseExpression()])

            elif Parser.tokens.actual.tp == "GREATER_THAN":
                node = BinOp(">",[node,Parser.parseExpression()])

            elif Parser.tokens.actual.tp == "LESS_THAN":
                node = BinOp("<",[node,Parser.parseExpression()])

        return node

    def parseType():

        if Parser.tokens.actual.tp == "INTEGER":
            Parser.tokens.selectNext()
            node = Type("INTEGER")

        elif Parser.tokens.actual.tp == "BOOLEAN":
            Parser.tokens.selectNext() 
            node = Type("BOOLEAN")
            
        else:
            raise ValueError("variable type not supported")

        return node

    def parseStatement():

        if Parser.tokens.actual.tp == "IDENTIFIER":
            variable_name = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

            if Parser.tokens.actual.tp == "EQUAL":
                Parser.tokens.selectNext()
                node = Assignment([variable_name, Parser.parseRelExpression()])
        
        elif Parser.tokens.actual.tp == "PRINT":
            Parser.tokens.selectNext()
            node = Print(Parser.parseExpression())

        elif Parser.tokens.actual.tp == "DIM":
            Parser.tokens.selectNext()

            if Parser.tokens.actual.tp == "IDENTIFIER":
                variable_name = Identifier(Parser.tokens.actual.value)        
                Parser.tokens.selectNext()

                if Parser.tokens.actual.tp == "AS":
                    Parser.tokens.selectNext()
                    node = VarDec([variable_name, Parser.parseType()])
                
                else:
                    raise ValueError(f"AS expected, got {Parser.tokens.actual.tp}")

            else:
              raise ValueError(f"IDENTIFIER expected, got {Parser.tokens.actual.tp}")

        elif Parser.tokens.actual.tp == "WHILE":

            Parser.tokens.selectNext()
            condition = Parser.parseRelExpression()
            
            if Parser.tokens.actual.tp == "BREAK_LINE":
                Parser.tokens.selectNext()
                statement = Parser.parseStatements()

                if Parser.tokens.actual.tp == "WEND":

                    node = While([condition,statement])
                    Parser.tokens.selectNext()

                else:
                    raise SyntaxError(f"WEND token expected, got {Parser.tokens.actual.value}")

            else:
                raise SyntaxError(f"must skip a line after while condition")

        elif Parser.tokens.actual.tp == "IF":
            
            Parser.tokens.selectNext()
            condition = Parser.parseRelExpression()
            
            if Parser.tokens.actual.tp == "THEN":
                Parser.tokens.selectNext()

                if Parser.tokens.actual.tp == "BREAK_LINE":
                    
                    if_statements = []

                    while Parser.tokens.actual.tp != "END" and Parser.tokens.actual.tp != "ELSE":
                        if_statements.append(Parser.parseStatement())

                        if Parser.tokens.actual.tp == "BREAK_LINE":
                            Parser.tokens.selectNext()
                        
                        else:
                            raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")


                    if Parser.tokens.actual.tp == "ELSE":
                        Parser.tokens.selectNext()
                        
                        if Parser.tokens.actual.tp == "BREAK_LINE":
                            Parser.tokens.selectNext()
                        
                        else:
                            raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")

                        else_statements = []

                        while Parser.tokens.actual.tp != "END":
                            else_statements.append(Parser.parseStatement())

                            if Parser.tokens.actual.tp == "BREAK_LINE":
                                Parser.tokens.selectNext()
                        
                            else:
                                raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")
                    
                        Parser.tokens.selectNext()
                            
                        if Parser.tokens.actual.tp == "IF":
                            node = If([condition,if_statements,else_statements])
                            Parser.tokens.selectNext()

                        else:
                            raise SyntaxError(f"IF token expected, got {Parser.tokens.actual.value}")
                    else:
                        raise SyntaxError(f"ELSE token expected, got {Parser.tokens.actual.value}")
                else:
                    raise SyntaxError(f"must skip a line after THEN token")    
            else:
                raise SyntaxError(f"THEN token expected, got {Parser.tokens.actual.value}")
        else:
            return NoOp(None)

        return node 

    def program():

        statements = []

        if Parser.tokens.actual.tp == "SUB":
            Parser.tokens.selectNext()

            if Parser.tokens.actual.tp == "MAIN":
                Parser.tokens.selectNext()

                if Parser.tokens.actual.tp == "OPENP":
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.tp == "CLOSEP":
                        Parser.tokens.selectNext()

                        if Parser.tokens.actual.tp == "BREAK_LINE":
                            Parser.tokens.selectNext()

                            while Parser.tokens.actual.tp != "END":
                                statements.append(Parser.parseStatement())

                                if Parser.tokens.actual.tp == "BREAK_LINE":
                                    Parser.tokens.selectNext()

                                else:
                                  raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")
                            
                            Parser.tokens.selectNext()

                            if Parser.tokens.actual.tp == "SUB":
                                Parser.tokens.selectNext()
                            
                            else:
                                raise ValueError(f"SUB expected, got {Parser.tokens.actual.tp}")
                        else:
                            raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")
                    else:
                        raise ValueError(f"CLOSEP expected, got {Parser.tokens.actual.tp}")                    
                else:
                    raise ValueError(f"OPENP expected, got {Parser.tokens.actual.tp}")
            else:
                raise ValueError(f"MAIN expected, got {Parser.tokens.actual.tp}")
        else:
            raise ValueError(f"SUB expected, got {Parser.tokens.actual.tp}")

        return Program(statements)

with open(sys.argv[1], 'r') as myfile:
    source = myfile.read()
#print(source)

Parser.run(source)