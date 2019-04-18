import re

class PrePro():

    def filter(source):
        
        return re.sub("'.*\n", "\n", source).lower()