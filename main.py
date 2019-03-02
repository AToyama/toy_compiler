# COMPILER PYTHON

source = input("expression:\n")

OPS = {
    "+" : "PLUS",
    "-" : "MINUS",
    "*" : "MULT",
    "/" : "DIV"
}

class PrePro():

    def spaces(Source):
        return  ''.join(source.split())

    def filter(source):

        temp_source = source

        occurencies = source.count("'")
        idxs = [i for i, a in enumerate(source) if a == "'"]

        for i in range(occurencies):
            idx = temp_source.find("'")
            idx_count = idx
            
            while idx_count < len(temp_source):
                if source[idx_count] == "\\":
                    if source[idx_count + 1] == "n" or source[idx_count + 1] == "r":
                        idx_count += 2
                        break
                        
                idx_count += 1
            
            temp_source = temp_source[:idx] + temp_source[idx_count:]

        return temp_source

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
                raise ValueError(f"{self.origin[self.position]} is not a number")   

        else:

            token = Token("EOF", None)

        self.actual = token

        print(self.actual.tp,self.actual.value)


class Parser():

    tokens = None

    def run(source):
        Parser.tokens = Tokenizer(source)
        #Parser.tokens.selectNext()

    def parseTerm():

        Parser.tokens.selectNext()
        
        if Parser.tokens.actual.tp == "INT":

            result = int(Parser.tokens.actual.value)

            Parser.tokens.selectNext()

            while Parser.tokens.actual.tp == "DIV" or Parser.tokens.actual.tp == "MULT":
 
                if Parser.tokens.actual.tp == "DIV":
                    
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tp == "INT":
                        result //= Parser.tokens.actual.value
                    else:
                        # not a number after an operator
                        raise ValueError("Invalid Input")

                elif Parser.tokens.actual.tp == "MULT":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.tp == "INT":
                        result *= Parser.tokens.actual.value
                    else:
                        # not a number after an operator
                        raise ValueError("Invalid Input")
                else:
                    raise ValueError(f"{Parser.tokens.actual.value} is not a valid Operator")

                Parser.tokens.selectNext()

        else:
            raise ValueError(f"{Parser.tokens.actual.value} is not a number")   

        return result 


    def parseExpression():

        #print(Parser.tokens.actual.tp)
        result = Parser.parseTerm()

        while Parser.tokens.actual.tp != "EOF" :

            if Parser.tokens.actual.tp == "PLUS":
                result += Parser.parseTerm()

            elif Parser.tokens.actual.tp == "MINUS":
                result -= Parser.parseTerm()

            else:
                raise ValueError(f"{Parser.tokens.actual.value} is not a valid Operator")

        return result

source = PrePro.spaces(source)
source = PrePro.filter(source)
Parser.run(source)
print(Parser.parseExpression())
