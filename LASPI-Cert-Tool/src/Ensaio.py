from pkcs11 import Token
from threading import Lock
from time import sleep

from src.defines import SLEEP_THREAD_TIME, COLUMN_WIDTH, COLUMN_SEPARATOR, END_SECTION_LINE
from src.Requirements import REQUISITOS_CARTAO, REQUISITOS_TOKEN


class Ensaio():
    def __init__(self, test_label : str, module_type : str, **kwargs):
        self.pin = kwargs["pin"]
        self.puk = kwargs["puk"]
        
        self.test_label = test_label
        self.type = module_type

    def __call__(self, tokens : dict[Lock, Token]):

        lock_acquired = None
        while lock_acquired == None:
            lock_acquired = self.__getTokenAvailable(tokens)
            sleep(SLEEP_THREAD_TIME)
        
        lock_acquired.acquire()
        print(f" Requisito {self.test_label} ".center(COLUMN_WIDTH, COLUMN_SEPARATOR))
        try:
            if self.type == "card":
                REQUISITOS_CARTAO[self.test_label](token=tokens[lock_acquired], pin=self.pin, puk=self.puk)
            elif self.type == "token":
                REQUISITOS_TOKEN[self.test_label](token=tokens[lock_acquired], pin=self.pin, puk=self.puk)
            else:
                raise Exception("Tipo de módulo não reconhecido.")
        except Exception as e:
            print(e)

        lock_acquired.release()
        print(END_SECTION_LINE)
        
    def __getTokenAvailable(self, tokens : dict[Lock, Token]):
        for lock, token in tokens.items():
            if not lock.locked():
                return lock
        return None