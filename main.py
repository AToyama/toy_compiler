# COMPILER PYTHON

# - colocar EOF no run
# - while not + ou - no expression

source = input("expression:\n")

OPS = {
    "+" : "PLUS",
    "-" : "MINUS",
    "*" : "MULT",
    "/" : "DIV",
    "(" : "OPENP",
    ")" : "CLOSEP"
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

            elif self.origin[self.position] in OPS:

                token = Token(OPS[self.origin[self.position]],self.origin[self.position])
                self.position += 1


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
        Parser.tokens = Tokenizer(source)

    def parseFactor():

        Parser.tokens.selectNext()

        if Parser.tokens.actual.tp == "INT":
            result = int(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.tp == "PLUS":
            result = Parser.parseFactor()

        elif Parser.tokens.actual.tp == "MINUS":
            result = -Parser.parseFactor()

        elif Parser.tokens.actual.tp == "OPENP":
            result = Parser.parseExpression()

            if Parser.tokens.actual.tp != "CLOSEP":
                raise ValueError("Missing parentheses")
            else:
                Parser.tokens.selectNext()

        else:
            raise ValueError(f"{Parser.tokens.actual.value} not a valid operator")

        return result


    def parseTerm():

        result = Parser.parseFactor()

        while Parser.tokens.actual.tp == "DIV" or  Parser.tokens.actual.tp == "MULT":

            if Parser.tokens.actual.tp == "MULT":
                result *= Parser.parseFactor()

            elif Parser.tokens.actual.tp == "DIV":
                result //= Parser.parseFactor()

        return result


    def parseExpression():

        #print(Parser.tokens.actual.tp)
        result = Parser.parseTerm()

        while Parser.tokens.actual.tp == "PLUS" or  Parser.tokens.actual.tp == "MINUS":

            if Parser.tokens.actual.tp == "PLUS":
                result += Parser.parseTerm()

            elif Parser.tokens.actual.tp == "MINUS":
                result -= Parser.parseTerm()

        return result

source = PrePro.spaces(source)
source = PrePro.filter(source)
Parser.run(source)
print(Parser.parseExpression())
