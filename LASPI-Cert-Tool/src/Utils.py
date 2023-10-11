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
    for key in keys:
            try:
                # veja get_objects quando for implementar a parte de certificados e parâmetros

                # tenta acessar a chave
                key_retrieved = session.get_key(label=key.label, id=key.id, key_type=key.key_type, object_class=key.object_class)
                key_retrieved.destroy() # tenta deletar a chave
            except pkcs11.exceptions.NoSuchKey as e:
                # captura o erro ao não achar a chave
                print(e)
                continue
            except Exception as e:
                # captura o erro ao não conseguir destruir a chave (todos os tipos de chave devem cair aqui)
                print(e)
                continue
            else:
                # se acessar e deletar a chave e não for lançada nenhuma exceção, retorna False
                return False

    return True

def InitializeSlots(module : str, pin : str = "1234", puk : str = "12345678", base_name : str = "ensaios", slots : list = [0]):
    '''
        Inicializa os slots com os tokens disponíveis.
    '''

    utils_path = getcwd+"\LASPI_Utils.ps1"
    p = subprocess.Popen(["powershell.exe", f". {utils_path}; Initialize-Module -Module {module} -PIN {pin} -PUK {puk} -Name {base_name} -Slots @"+str(slots).replace("[", "(").replace("]", ")")], stderr=sys.stderr, stdout=sys.stdout)
    p.communicate()

    # recupera informações de todos os slots
        

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