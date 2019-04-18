class Node():

    def __init__(self):

        value = None
        children = []

    def Evaluate(self, symboltable):
        pass

class BinOp(Node):

    def __init__(self, value, children):

        self.value = value
        self.children = children

    def Evaluate(self, symboltable):

        if self.value == "+":
            return self.children[0].Evaluate(symboltable) + self.children[1].Evaluate(symboltable)
            
        elif self.value == "-":
            return self.children[0].Evaluate(symboltable) - self.children[1].Evaluate(symboltable)

        elif self.value == "*":
            return self.children[0].Evaluate(symboltable) * self.children[1].Evaluate(symboltable)

        elif self.value == "/":
            return self.children[0].Evaluate(symboltable) // self.children[1].Evaluate(symboltable)

        elif self.value == ">":
            return self.children[0].Evaluate(symboltable) > self.children[1].Evaluate(symboltable)
        
        elif self.value == "<":
            return self.children[0].Evaluate(symboltable) < self.children[1].Evaluate(symboltable)

        elif self.value == "=":
            return self.children[0].Evaluate(symboltable) == self.children[1].Evaluate(symboltable)

        elif self.value == "AND":
            return self.children[0].Evaluate(symboltable) and self.children[1].Evaluate(symboltable)

        elif self.value == "OR":
            return self.children[0].Evaluate(symboltable) or self.children[1].Evaluate(symboltable)

class UnOp(Node):

	def __init__(self, value, children):

		self.value = value
		self.children = children

def Evaluate(self, symboltable):
    
    if self.value == "+":
        return self.children.Evaluate(symboltable)
    
    elif self.value == "-":
        return - self.children.Evaluate(symboltable)
    
    elif self.value == "NOT":
        return not self.children.Evaluate(symboltable)

class IntVal(Node):

    def __init__(self, value):

        self.value = value

    def Evaluate(self, symboltable):

        return self.value

class NoOp(Node):

    def __init__(self, value):
        self.value = None

class Print(Node):

    def __init__(self, children):

        self.children = children

    def Evaluate(self, symboltable):

        print(self.children.Evaluate(symboltable))

class Assignment(Node):

    def __init__(self, children):

        self.children = children

    def Evaluate(self, symboltable):

        symboltable.setter(self.children[0].value, self.children[1].Evaluate(symboltable))

class Identifier(Node):
    
    def __init__(self, value):
        
        self.value = value

    def Evaluate(self, symboltable):

        return symboltable.getter(self.value)

class Statement(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, symboltable):

        for child in self.children:
            child.Evaluate(symboltable)

class Input(Node):

    #def __init__(self, value):
        
    #    self.value = value
    
    def Evaluate(self, symboltable):

        return int(input())

class If(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, symboltable):

        if self.children[0].Evaluate(symboltable):
            self.children[1].Evaluate(symboltable)
        else:
            if self.children[2]:
                self.children[2].Evaluate(symboltable)

class While(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, symboltable):
    
        while self.children[0].Evaluate(symboltable):
            self.children[1].Evaluate(symboltable)
