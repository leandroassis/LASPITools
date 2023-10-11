import argparse
import pkcs11
import os, sys
from threading import Thread, Lock

from src.Requirements import ParseRequirements
from src.defines import COLUMN_WIDTH, COLUMN_SEPARATOR, END_SECTION_LINE, REQS_POR_LINHA
from src.Utils import InitializeSlots
from src.Ensaio import Ensaio

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='Ferramenta desenvolvida por Leandro A. (leandro@laspi.ufrj.br)', prog="python CertTool.py")

    parser.add_argument('-m', '--module', type=str, help='PKCS#11 dll to interface with modules.', required=True)
    parser.add_argument('--pin', nargs=1, default="1234", type=str, help='User\'s PIN.')
    parser.add_argument('--puk', nargs=1, default="12345678", type=str, help='User PUK.')
    parser.add_argument('-n', '--name', type=str, nargs=1, default="ensaios", help='Base name for the token(s) labels.')
    parser.add_argument('-s', '--slots', type=int, nargs='+', help='Slots to be tested (e.g. -s 0, 1, 2, 3).', default=[0])
    parser.add_argument('--version', action='version', version='%(prog)s Release 1.0')
    parser.add_argument('-r', '--requirements', nargs="+", type=str, help='Requirements to be tested (e.g. -r II.7, II.9, II.10-II.15).', default=["All"])
    parser.add_argument('-t', '--type', nargs=1, type=str, help='Type of module to be tested (e.g. -t token, -t card).', default=["token"])
    parser.add_argument('-i', '--initialize', help='Initialize the token(s).', default=False, action='store_true')
    parser.add_argument('--redirect', help='Redirects the output to a file.', default=None, nargs=1, type=str)

    arguments = parser.parse_args()
    os.system("cls") # clean the screen
    print(arguments)
    print()
    
    if(arguments.redirect != None):
        sys.stdout = open(arguments.redirect[0], "w", encoding="utf-8")

    '''
    LIBRARY SECTION
    '''
    # Load the PKCS11 library
    lib = pkcs11.lib(arguments.module)

    if lib:
        print(f" Módulo \"{arguments.module}\" carregado com sucesso! ".center(COLUMN_WIDTH, COLUMN_SEPARATOR))
        print()
        print("Fabricante: "+lib.manufacturer_id)

        str_version = ".".join(list(map(lambda x : str(x), lib.library_version)))
        str_crypto_version = ".".join(list(map(lambda x : str(x), lib.cryptoki_version)))
        print("Versão do módulo: " + str_version)
        print("Descrição do módulo: " + lib.library_description)
        print("Versão do Cryptoki: " + str_crypto_version)
        print(END_SECTION_LINE)        
    '''
    END LIBRARY SECTION
    '''

    '''
    SLOT SECTION
    '''
    print(" Slots para realização de testes ".center(COLUMN_WIDTH, COLUMN_SEPARATOR))
    print()

    # Reads the slots available 
    slots = lib.get_slots(token_present=True)

    # only uses the slots specified by the user
    try:
        slots = list(map(lambda x : slots[x], arguments.slots))
    except IndexError:
        print("Erro: um ou mais slots especificados não existem!")
        print("Lista dos slots disponíveis: " + str([x for x in range(len(slots))]).replace("[", "").replace("]", ""))
        print(END_SECTION_LINE)
        exit(1)

    # for each slot, get hardware and firmware versions
    for idx, slot in enumerate(slots):
        str_hw_version = ".".join(list(map(lambda x : str(x), slot.hardware_version)))
        str_fw_version = ".".join(list(map(lambda x : str(x), slot.firmware_version)))
        
        print("Slot " + str(idx))
        print("ID: " + str(slot.slot_id))
        print("Fabricante: " + slot.manufacturer_id)
        print("Versão de hardware: " + str_hw_version)
        print("Versão de firmware: " + str_fw_version)
        print("Flags: " + str(slot.flags))

        print() if idx != len(slots)-1 else None
    print(END_SECTION_LINE)
    '''
    END SLOT SECTION
    '''

    '''
    REQUIRIMENTS SECTION
    '''
    # parses the requirements
    requirements = ParseRequirements(arguments.requirements, arguments.type[0])
    
    print(" Conjunto de ensaios ".center(COLUMN_WIDTH, COLUMN_SEPARATOR))
    print()
    
    str_requirements = ""
    for idx, requirement in enumerate(requirements):
        if idx%REQS_POR_LINHA == 0 and idx != 0:
            str_requirements += "\n"
        str_requirements += requirement
        str_requirements += "" if idx == len(requirements)-1 else ", "
    
    print(str_requirements)

    print(END_SECTION_LINE)
    '''
    END REQUIRIMENTS SECTION
    '''

    print(" Início das operações ".center(COLUMN_WIDTH, COLUMN_SEPARATOR))
    print()

    # initialize the slots
    if arguments.initialize:
        print(" Inicialização dos módulos ".center(COLUMN_WIDTH, COLUMN_SEPARATOR))
        print()
        InitializeSlots(arguments.module, arguments.pin, arguments.puk, arguments.name, arguments.slots)
        print(END_SECTION_LINE)

    # creates a dictionary of tokens and locks
    tokens = {}
    for slot in slots:
        tokens[Lock()] = slot.get_token()
    
    # creates the Ensaio objects and the threads for each requirement
    threads = []
    for ensaio in list(map(lambda x : Ensaio(x, arguments.type[0], pin=arguments.pin, puk=arguments.puk), requirements)):
        threads.append(Thread(target=ensaio, args=(tokens,)))
        threads[-1].start() # starts the thread

    # waits for all threads to finish
    for thread in threads:
        thread.join()

    print(" Fim das operações ".center(COLUMN_WIDTH, COLUMN_SEPARATOR))