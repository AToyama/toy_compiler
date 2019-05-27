def write_line(line):
    file = open("source_code.asm", "a", encoding="utf-8")
    file.write(line + "\n")
    file.close()

class Node():

    i = -1

    def __init__(self):

        self.value = None
        self.children = []
        self.id =  Node.newId()

    def Evaluate(self, symboltable):
        pass

    def newId():
        Node.i += 1
        return Node.i

class BinOp(Node):

    def __init__(self, value, children):
        super().__init__()
        self.value = value
        self.children = children

    def Evaluate(self, symboltable):

        left = self.children[0].Evaluate(symboltable)
        right = self.children[1].Evaluate(symboltable)

        write_line("PUSH EBX")
        write_line("POP EAX")

        if self.value == "+":
            write_line("ADD EAX, EBX")
            write_line("MOV EBX, EAX")
            return left + right
            
        elif self.value == "-":
            write_line("SUB EAX, EBX")
            write_line("MOV EBX, EAX")
            return left - right

        elif self.value == "*":
            write_line("IMUL EBX")
            write_line("MOV EBX, EAX")
            return left * right

        elif self.value == "/":
            write_line("IDIV EBX")
            write_line("MOV EBX, EAX")
            return left // right

        elif self.value == ">":
            write_line("CMP EAX, EBX")
            write_line("CALL binop_jg")
            return left > right
        
        elif self.value == "<":
            write_line("CMP EAX, EBX")
            write_line("CALL binop_jl")          
            return left < right

        elif self.value == "=":
            write_line("CMP EAX, EBX")
            write_line("CALL binop_je")
            return left == right

        elif self.value == "AND":
            write_line("AND EAX, EBX")
            write_line("MOV EBX, EAX")
            return left and right

        elif self.value == "OR":
            write_line("OR EAX, EBX")
            write_line("MOV EBX, EAX")
            return left or right

class UnOp(Node):

	def __init__(self, value, children):

		self.value = value
		self.children = children

def Evaluate(self, symboltable):
    
    value = self.children.Evaluate(symboltable)

    if self.value == "+":
        return value
    
    elif self.value == "-":
        return - value
    
    elif self.value == "NOT":

        if value[0]:
            write_line("MOV EBX, False")
        else:
            write_line("MOV EBX, True")

        return not value

class IntVal(Node):

    def __init__(self, value):

        self.value = value

    def Evaluate(self, symboltable):

        if self.value == "TRUE":
            write_line(f"MOV EBX, True")

        elif self.value == "FALSE":
            write_line(f"MOV EBX, False")

        else:
            write_line(f"MOV EBX, { self.value }")
        return self.value

class NoOp(Node):

    def __init__(self, value):
        self.value = None

class Print(Node):

    def __init__(self, children):

        self.children = children

    def Evaluate(self, symboltable):

        write_line("PUSH EBX")
        write_line("CALL print")
        write_line("POP EBX")

        print(self.children.Evaluate(symboltable))

class Assignment(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, symboltable):

        variable = symboltable.getter(self.children[0].value)
        variable_value = self.children[0].value
        variable_type = self.children[1].Evaluate(symboltable)
        
        if variable[1] == "BOOLEAN":
            if variable_type == "TRUE":
                write_line(f"MOV [EBP-True] , EBX")
            else:
                print(variable_type, "------------------")
                write_line(f"MOV [EBP-False] , EBX")

        else:
            write_line(f"MOV [EBP-{ variable[2]}] , EBX")


        symboltable.setter(variable_value, variable_type)

class Identifier(Node):
    
    def __init__(self, value):
        
        self.value = value

    def Evaluate(self, symboltable):

        variable_value = symboltable.getter(self.value)
        write_line(f"MOV EBX, [EBP-{ variable_value[2] }]")

        return variable_value[0]

# class Statement(Node):

#     def __init__(self, children):
#         self.children = children

#     def Evaluate(self, symboltable):

#         for child in self.children:
#             child.Evaluate(symboltable)

class Input(Node):

    #def __init__(self, value):
        
    #    self.value = value
    
    def Evaluate(self, symboltable):
        
        input_value =  int(input())
        write_line(f"MOV EBX, { input_value }")
        
        return input_value

class If(Node):

    def __init__(self, children):
        super().__init__()
        self.children = children

    def Evaluate(self, symboltable):

        # condition assembly
        write_line(f"IF_{ self.id }:")
        self.children[0].Evaluate(symboltable)
        write_line("CMP EBX, False")
        write_line(f"JE EXIT_{ self.id }")

        if self.children[0].Evaluate(symboltable):
            for child in self.children[1]:
                child.Evaluate(symboltable)
            write_line(f"EXIT_{ self.id }:")
            
        else:
            for child in self.children[2]:
                child.Evaluate(symboltable)

class While(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, symboltable):

        # condition assembly
        write_line(f"LOOP_{ self.id }")
        self.children[0].Evaluate(symboltable)
        write_line(f"CMP EBX, False")
        write_line(f"EXIT_{ self.id }")

        while self.children[0].Evaluate(symboltable):
            self.children[1].Evaluate(symboltable)

        write_line(f"JMP LOOP_{ self.id }")
        write_line(f"EXIT_{ self.id }:")

class Type(Node):
    
    def __init__(self, value):
        
        self.value = value    

    def Evaluate(self, symboltable):

        return self.value

class BoolVal(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self, st):
        

        if self.value == "TRUE":
            write_line(f"MOV EBX, True")
            return (True, "BOOLEAN")

        elif self.value == "FALSE":
            write_line(f"MOV EBX, False")
            return (False, "BOOLEAN")

class VarDec(Node):

    def __init__(self, children):
        self.children = children

    def Evaluate(self, st):
        variable_name = self.children[0].value
        variable_type = self.children[1].Evaluate(st)
        shift = st.declare(variable_name, variable_type)
        if variable_type in ["ITNEGER","BOOLEAN"]:
            write_line(f"PUSH DWORD 0 ; Dim { variable_name } as { variable_type } [EBP-{ shift }]")

class Program(Node):
    
    def __init__(self, children):
        self.children = children

    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)
