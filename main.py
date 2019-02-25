# COMPILER PYTHON

source = input("expression:\n")
source = ''.join(source.split())


OPS = {
    "+" : "PLUS",
    "-" : "MINUS"
}

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
        if self.position < len(self.origin):

            if self.origin[self.position].isdigit():
                
                num = ""
    
                while self.origin[self.position].isdigit():

                    num += self.origin[self.position]
                    self.position += 1

                    if self.position  == len(self.origin):
                        break
                    
                token = Token("INT",int(num))

            elif self.origin[self.position] in OPS:

                token = Token(OPS[self.origin[self.position]],self.origin[self.position])
                self.position += 1


            else:

                # Invalid Token
                raise ValueError("Invalid Input")

        else:

            token = Token("EOF", None)

        self.actual = token

        #print(self.actual.tp,self.actual.value)

class Parser():

    tokens = None

    def run(source):
        Parser.tokens = Tokenizer(source)
        Parser.tokens.selectNext()

    def parseExpression():
        
        result = None
        
        if Parser.tokens.actual.tp == "INT":

            result = int(Parser.tokens.actual.value)

            Parser.tokens.selectNext()

            while Parser.tokens.actual.tp in OPS.values():
 
                if Parser.tokens.actual.tp == "PLUS":
                    
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tp == "INT":
                        result += Parser.tokens.actual.value
                    else:
                        # not a number after an operator
                        raise ValueError("Invalid Input")

                elif Parser.tokens.actual.tp == "MINUS":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tp == "INT":
                        result -= Parser.tokens.actual.value
                    else:
                        # not a number after an operator
                        raise ValueError("Invalid Input")
                else:
                    raise ValueError(f"{Parser.tokens.actual.value} is not a valid Operator")

                Parser.tokens.selectNext()

        else:
            raise ValueError(f"{Parser.tokens.actual.value} is not a number")   

        return result 


Parser.run(source)
print(Parser.parseExpression())