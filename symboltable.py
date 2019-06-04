class SymbolTable():

    def __init__(self, parent):
        self.symbol_table = {}
        self.parent = parent

    def declare(self, variable_name, variable_type):

        if variable_name not in self.symbol_table.keys():
            self.symbol_table[variable_name] = [None, variable_type]

        else:
          raise ValueError(f"{variable_name} already exists as a variable")


    def setter(self, variable_name, value):
        
        if variable_name in self.symbol_table.keys():
            self.symbol_table[variable_name][0] = value

        else:
            raise ValueError(f"{variable_name} not declared")

    def getter(self, variable):


        # print(variable,self.symbol_table)
        if variable in self.symbol_table.keys():
            if self.symbol_table[variable][0] == None:
                return self.parent.getter(variable)
            else:
                return self.symbol_table[variable]

        else:
            if self.parent != None:
                return self.parent.getter(variable)
            else:
                raise NameError(f"{variable} does not exist ")

    def create(self, variable_name, variable_value, variable_type):

        self.symbol_table[variable_name] = [variable_value, variable_type]