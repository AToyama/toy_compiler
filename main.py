# COMPILER PYTHON

# update parser
# mydict.keys()[mydict.values().index(value)]

# v2.3

from node import Node, BinOp, UnOp, IntVal, NoOp, Print, Assignment, Statement, Identifier, Input, While, If, VarDec, Type, BoolVal, Program, FuncDec, SubDec, FuncCall
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
    ">" : "GREATER_THAN",
    "," : "COMMA",
}

RESERVED = ['call','function','input','print','begin','end','and','or','not','while','wend','if','then','else','dim','true','false','sub','as','boolean','integer']

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

        # print(self.actual.tp,self.actual.value)


class Parser():

    tokens = None

    @staticmethod
    def run(source):

        source = PrePro.filter(source)
        Parser.tokens = Tokenizer(source)
        Parser.tokens.selectNext()

        st = SymbolTable(None)

        Parser.program().Evaluate(st)
        
        if Parser.tokens.actual.tp != "EOF":
            raise ValueError(f"{Parser.tokens.actual.value} invalid at end of sentence")

    def parseFactor():

        #Parser.tokens.selectNext()

        if Parser.tokens.actual.tp == "INT":
            node = IntVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.tp == "PLUS":
            Parser.tokens.selectNext()
            node = UnOp("+",Parser.parseFactor())

        elif Parser.tokens.actual.tp == "MINUS":
            Parser.tokens.selectNext()
            node = UnOp("-",Parser.parseFactor())
        
        elif Parser.tokens.actual.tp == "NOT":
            Parser.tokens.selectNext()
            node = UnOp("NOT",Parser.parseFactor())

        elif Parser.tokens.actual.tp in ["TRUE","FALSE"]:
            node = BoolVal(Parser.tokens.actual.tp)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.tp == "OPENP":
            Parser.tokens.selectNext()
            node = Parser.parseRelExpression()

            if Parser.tokens.actual.tp != "CLOSEP":
                raise ValueError("Missing parentheses")
            else:
                Parser.tokens.selectNext()
        
        elif Parser.tokens.actual.tp == "IDENTIFIER":
            var_name = Parser.tokens.actual.value
            Parser.tokens.selectNext()
              
            if Parser.tokens.actual.tp == "OPENP":
                parameters = []
                Parser.tokens.selectNext()

                while Parser.tokens.actual.tp != "CLOSEP":
                    parameters.append(Parser.parseRelExpression())
                    
                    if Parser.tokens.actual.tp == "COMMA":
                        Parser.tokens.selectNext()

                    else:
                        break

                if Parser.tokens.actual.tp != "CLOSEP":
                    raise ValueError("Missing parentheses")
                node = FuncCall(var_name,parameters)
                Parser.tokens.selectNext()           

            else:
                node = Identifier(var_name)            

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
                Parser.tokens.selectNext()
                node = BinOp("+",[node,Parser.parseTerm()])

            elif Parser.tokens.actual.tp == "MINUS":
                Parser.tokens.selectNext()
                node = BinOp("-",[node,Parser.parseTerm()])

            elif Parser.tokens.actual.tp == "OR":
                Parser.tokens.selectNext()
                node = BinOp("OR",[node,Parser.parseTerm()])

        return node

    def parseRelExpression():

        node = Parser.parseExpression()

        if Parser.tokens.actual.tp in ["EQUAL","GREATER_THAN","LESS_THAN"]:

            if Parser.tokens.actual.tp == "EQUAL":
                Parser.tokens.selectNext()
                node = BinOp("=",[node,Parser.parseExpression()])

            elif Parser.tokens.actual.tp == "GREATER_THAN":
                Parser.tokens.selectNext()
                node = BinOp(">",[node,Parser.parseExpression()])

            elif Parser.tokens.actual.tp == "LESS_THAN":
                Parser.tokens.selectNext()
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
            variable_name = Parser.tokens.actual.value
            Parser.tokens.selectNext()

            if Parser.tokens.actual.tp == "EQUAL":
                Parser.tokens.selectNext()
                node = Assignment([Identifier(variable_name), Parser.parseRelExpression()])

            elif Parser.tokens.actual.tp == "OPENP":
                parameters = []
                Parser.tokens.selectNext()

                while Parser.tokens.actual.tp != "CLOSEP":
                    parameters.append(Parser.parseRelExpression())
                    
                    if Parser.tokens.actual.tp == "COMMA":
                        Parser.tokens.selectNext()

                    else:
                        break

                if Parser.tokens.actual.tp != "CLOSEP":
                    raise ValueError("Missing parentheses")

                node = FuncCall(variable_name,parameters)
                Parser.tokens.selectNext()

            else:
                raise ValueError(f"EQUAL token expected, got {Parser.tokens.actual.tp}")

        
        elif Parser.tokens.actual.tp == "PRINT":
            Parser.tokens.selectNext()
            node = Print(Parser.parseRelExpression())

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
                statements = []

                while Parser.tokens.actual.tp != "WEND":
                    statements.append(Parser.parseStatement())

                    if Parser.tokens.actual.tp == "BREAK_LINE":
                        Parser.tokens.selectNext()

                    else:
                        raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")

                Parser.tokens.selectNext()
                node = While([condition, statements])

                if Parser.tokens.actual.tp == "BREAK_LINE":
                    Parser.tokens.selectNext()

                else:
                    raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")
              
                    
                # else:
                #     raise SyntaxError(f"WEND token expected, got {Parser.tokens.actual.value}")

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
                    
                    elif Parser.tokens.actual.tp == "END":

                        Parser.tokens.selectNext()
                            
                        if Parser.tokens.actual.tp == "IF":
                            node = If([condition,if_statements])
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

    def funcDec():

        statements = []
        parameters = []

        if Parser.tokens.actual.tp == "IDENTIFIER":
            
            func_name = Parser.tokens.actual.value

            Parser.tokens.selectNext()

            if Parser.tokens.actual.tp == "OPENP":
                Parser.tokens.selectNext()

                while Parser.tokens.actual.tp != "CLOSEP":
                    
                    if Parser.tokens.actual.tp == "IDENTIFIER":
                        var_name = Parser.tokens.actual.value
                        Parser.tokens.selectNext()

                        if Parser.tokens.actual.tp == "AS":
                            Parser.tokens.selectNext()

                            if Parser.tokens.actual.tp in ["INTEGER","BOOLEAN"]:
                                parameters.append((var_name, Parser.tokens.actual.tp))
                                Parser.tokens.selectNext()

                                if Parser.tokens.actual.tp == "COMMA":
                                    Parser.tokens.selectNext()
                                else:
                                    break

                            else:
                                raise SyntaxError(f"type expected, got {Parser.tokens.actual.value}")
                        
                        else:
                            raise SyntaxError(f"AS token expected, got {Parser.tokens.actual.value}")


                    else:
                        raise SyntaxError(f"IDENTIFIER token expected, got {Parser.tokens.actual.value}")

                if Parser.tokens.actual.tp != "CLOSEP":
                    raise SyntaxError(f"CLOSEP token expected, got {Parser.tokens.actual.value}")

                Parser.tokens.selectNext()

                if Parser.tokens.actual.tp == "AS":
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.tp in ["INTEGER","BOOLEAN"]:
                        func_type = Parser.tokens.actual.tp
                        Parser.tokens.selectNext()

                    else:
                        raise SyntaxError(f"type expected, got {Parser.tokens.actual.value}")
                
                else:
                    raise SyntaxError(f"AS token expected, got {Parser.tokens.actual.value}")

                if Parser.tokens.actual.tp == "BREAK_LINE":
                    Parser.tokens.selectNext()

                    while Parser.tokens.actual.tp != "END":
                        statements.append(Parser.parseStatement())

                        if Parser.tokens.actual.tp == "BREAK_LINE":
                            Parser.tokens.selectNext()

                        else:
                          raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")
                    
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.tp == "FUNCTION":
                        Parser.tokens.selectNext()

                        while Parser.tokens.actual.tp == "BREAK_LINE":
                            Parser.tokens.selectNext()

                    else:
                        raise ValueError(f"FUNCTION expected, got {Parser.tokens.actual.tp}")
                else:
                    raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")

                return FuncDec([(func_name, func_type),parameters,statements])

            else:
                raise SyntaxError(f"OPENP token expected, got {Parser.tokens.actual.value}")


    def subDec():

        statements = []
        parameters = []

        if Parser.tokens.actual.tp == "IDENTIFIER":
            
            sub_name = Parser.tokens.actual.value

            Parser.tokens.selectNext()

            if Parser.tokens.actual.tp == "OPENP":
                Parser.tokens.selectNext()

                while Parser.tokens.actual.tp != "CLOSEP":
                    
                    if Parser.tokens.actual.tp == "IDENTIFIER":
                        var_name = Parser.tokens.actual.value
                        Parser.tokens.selectNext()

                        if Parser.tokens.actual.tp == "AS":
                            Parser.tokens.selectNext()

                            if Parser.tokens.actual.tp in ["INTEGER","BOOLEAN"]:
                                parameters.append((var_name, Parser.tokens.actual.tp))
                                Parser.tokens.selectNext()

                                if Parser.tokens.actual.tp == "COMMA":
                                    Parser.tokens.selectNext()
                                else:
                                    break

                            else:
                                raise SyntaxError(f"type expected, got {Parser.tokens.actual.value}")
                        
                        else:
                            raise SyntaxError(f"AS token expected, got {Parser.tokens.actual.value}")


                    else:
                        raise SyntaxError(f"IDENTIFIER token expected, got {Parser.tokens.actual.value}")

                if Parser.tokens.actual.tp != "CLOSEP":
                    raise SyntaxError(f"CLOSEP token expected, got {Parser.tokens.actual.value}")

                Parser.tokens.selectNext()

                if Parser.tokens.actual.tp == "BREAK_LINE":
                    Parser.tokens.selectNext()

                    while Parser.tokens.actual.tp != "END":
                        statements.append(Parser.parseStatement())

                        if Parser.tokens.actual.tp == "BREAK_LINE":
                            Parser.tokens.selectNext()
                        
                        elif Parser.tokens.actual.tp == "END":
                            break

                        else:
                          raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")
                    
                    Parser.tokens.selectNext()

                    if Parser.tokens.actual.tp == "SUB":
                        Parser.tokens.selectNext()

                        while Parser.tokens.actual.tp == "BREAK_LINE":
                            Parser.tokens.selectNext()

                    else:
                        raise ValueError(f"SUB expected, got {Parser.tokens.actual.tp}")
                else:
                    raise ValueError(f"BREAK_LINE expected, got {Parser.tokens.actual.tp}")
           
                return SubDec([sub_name , parameters, statements])

            else:
                raise SyntaxError(f"OPENP token expected, got {Parser.tokens.actual.value}")


    def program():

        statements = []

        while Parser.tokens.actual.tp == "BREAK_LINE":
            Parser.tokens.selectNext()

        while Parser.tokens.actual.tp in ["SUB","FUNCTION"]:
            
            if Parser.tokens.actual.tp == "SUB":
                Parser.tokens.selectNext()
                statements.append(Parser.subDec())

            else:
                Parser.tokens.selectNext()
                statements.append(Parser.funcDec())

        statements.append(FuncCall("main",[]))

        return Program(statements)

with open(sys.argv[1], 'r') as myfile:
    source = myfile.read()
#print(source)

Parser.run(source)