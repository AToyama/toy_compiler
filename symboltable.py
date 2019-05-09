class SymbolTable():

    def __init__(self):
        self.symbol_table = {}


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
        
        if variable in self.symbol_table.keys():
            return self.symbol_table[variable][0]

        else:
            raise NameError(f"{variable} does not exist ")