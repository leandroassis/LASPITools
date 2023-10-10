import argparse
import pkcs11
from src.Utils import ParseRequirements

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ferramenta desenvolvida por Leandro A. (leandro@laspi.ufrj.br)', prog="python CertTool.py")

    parser.add_argument('-m', '--module', type=str, help='Module to be tested', required=True)
    parser.add_argument('--pin', nargs="?", default="1234", type=str, help='User\'s PIN')
    parser.add_argument('--puk', nargs="?", default="12345678", type=str, help='User PUK')
    parser.add_argument('-n', '--name', type=str, nargs="?", default="ensaios", help='Base name for the token(s) labels.')
    parser.add_argument('-s', '--slots', type=int, nargs='+', help='Slots to be tested (e.g. -s 0, 1, 2, 3)', default=0)
    parser.add_argument('--version', action='version', version='%(prog)s Release 1.0')
    parser.add_argument('-r', '--requirements', action="extend", nargs="+", type=str, help='Requirements to be tested (e.g. -r II.7, II.9, II.10-II.15', required=True, const="All")

    arguments = parser.parse_args()
    print(arguments)
    requirements = ParseRequirements(arguments.requirements)
    print(requirements)
    exit(1)
    # Load the PKCS11 library
    lib = pkcs11.lib(arguments.module)

    if lib:
        print("Módulo carregado com sucesso!")
        print("Fabricante: "+lib.manufacturer_id)

        str_version = ".".join(list(map(lambda x : str(x), lib.library_version)))
        str_crypto_version = ".".join(list(map(lambda x : str(x), lib.cryptoki_version)))
        print("Versão do módulo: " + str_version)
        print("Descrição do módulo: " + lib.library_description)
        print("Versão do Cryptoki: " + str_crypto_version)
        

    # Reads the slots available 
    slots = lib.get_slots(token_present=True)

    # only uses the slots specified by the user
    slots = list(filter(lambda x : x.slot_id in arguments.slots, slots))

    # for each slot, get hardware and firmware versions
    for slot in slots:
        str_hw_version = ".".join(list(map(lambda x : str(x), slot.hardware_version)))
        str_fw_version = ".".join(list(map(lambda x : str(x), slot.firmware_version)))
        
        print("===== Slot: " + str(slot.slot_id) + " =====")
        print("Versão de hardware: " + str_hw_version)
        print("Versão de firmware: " + str_fw_version)


    # parses the requirements
    requirements = ParseRequirements(arguments.requirements)
    


