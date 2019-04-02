class SymbolTable():

    def __init__(self):
        self.symbol_table = {}

    def setter(self, variable_name, value):
        
        self.symbol_table[variable_name] = value

    def getter(self, variable):
        
        if variable in self.symbol_table.keys():
            return self.symbol_table[variable]

        else:
            raise NameError(f"{variable} is not defined ")