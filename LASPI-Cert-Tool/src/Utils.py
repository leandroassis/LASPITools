import pkcs11
from pkcs11.constants import ObjectClass
import random as rd

import subprocess, sys
from os import getcwd

def Get_Tokens(lib : pkcs11.lib) -> list:
    '''
        Verifica todos os tokens disponíveis, lista seus slots e apresenta as informações de cada um. Retorna uma lista de tokens disponíveis na biblioteca passada como parâmetro.
    '''
    pass


def AcessDestroyKeys(keys : list, session : pkcs11.Session) -> bool:
    '''
        Recebe uma lista de chaves e tenta acessá-las e destruí-las.
        Retorna True se não conseguir acessar e destruir nenhuma chave, False caso contrário.
    '''

    print(f"Sessão de {str(session.user_type)} aberta com r/w.")

    for key in keys:
            try:
                # veja get_objects quando for implementar a parte de certificados e parâmetros
                print(f"Tentando acessar a chave {key.label} de id {key.id} do tipo {key.key_type}.")
                # tenta acessar a chave
                key_retrieved = session.get_key(label=key.label, id=key.id, key_type=key.key_type, object_class=key.object_class)

                print(f"Tentando destruir a chave {key.label} de id {key.id} do tipo {key.key_type}.")
                key_retrieved.destroy() # tenta deletar a chave
            except pkcs11.exceptions.NoSuchKey:
                # captura o erro ao não achar a chave
                print("Chave não encontrada.")
                continue
            except Exception as e:
                # captura o erro ao não conseguir destruir a chave (todos os tipos de chave devem cair aqui)
                print("Não foi possível destruir a chave.")
                continue
            else:
                # se acessar e deletar a chave e não for lançada nenhuma exceção, retorna False
                print(f"Chave {key.label} de id {key.id} do tipo {key.key_type} acessada e destruída.")

    print(f"Sessão de {str(session.user_type)} fechada.")
    return True

def InitializeSlots(module : str, pin : str = "1234", puk : str = "12345678", base_name : str = "ensaios", slots : list = [0]):
    '''
        Inicializa os slots com os tokens disponíveis.
    '''
    str_slots = str(slots).replace("[", "").replace("]", "")
    if len(slots) != 1:
        print(f"Inicializando os slots {str_slots} ...")
    else:
        print(f"Inicializando o slot {str_slots} ...")

    utils_path = getcwd()+"\src\LASPI_Utils.ps1"
    p = subprocess.Popen(["powershell.exe", f". {utils_path}; Initialize-Module -Module {module} -PIN {pin} -PUK {puk} -Name {base_name} -Slots @"+str(slots).replace("[", "(").replace("]", ")")], stderr=sys.stderr, stdout=sys.stdout)
    p.communicate()

    print("Fim da inicialização dos slots. Verifique o arquivo de log \"Logs\\Initialize-Module.log\" para mais informações.")

'''
To DO: Repassar ideia para o python

function Start-Tests(){
    param(
        [Paramater()]
        [array]$Slots=@(0),
        [Paramater(Mandatory=$true)]
        [array]$Tests
    )

    New-Item -ItemType Directory ".\Logs" -Force

    # parseia os ensaios realizados
    # inicializa os modulos

    # lista todos os mecanismos e escolhe um para assimétrico e um para simétrico
    # todo: faz duas listas com TODOS os tipos simétricos e assimétricos, realiza a geração de todos os tipos

    # cria as jobs com os ensaios
    # serializa as jobs baseado nos slots vagos
}
'''