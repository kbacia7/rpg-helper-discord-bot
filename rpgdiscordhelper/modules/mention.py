class Mention():
    def __init__(self):
       pass

    def get_int(self, mention_str):
       parsed =  int(mention_str[2:-1])
       return parsed