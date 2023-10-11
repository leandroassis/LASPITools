from pkcs11 import Token

class Ensaios():
    def __init__(self, name : str, token : Token, function, **kwargs):
        self.name = name
        self.function = function
        self.pin = kwargs["pin"]
        self.puk = kwargs["puk"]
        self.token = token

    def run_test(self):

        self.function(self.kwargs)