class ArgParser():
    def __init__(self):
        pass

    def parse(self, string):
        string = string[1:]
        return string.split(" ")
