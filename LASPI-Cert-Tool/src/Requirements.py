import pkcs11
from pkcs11.constants import MechanismFlag
from pkcs11.mechanisms import Mechanism
import random as rd

from src.defines import APPROVED_KEY_GEN_MECHANISMS, APPROVED_CERT_GEN_MECHANISMS, APPROVED_PARAM_GEN_MECHANISMS
from src.Utils import AcessDestroyKeys

# TO DO: ADICIONAR INFORMAÇÕES DE LOG EM TODOS AS FUNÇÕES


'''
    TESTS DEFINE SECTION
'''
def testsAccessObjects(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    '''
        Gera uma chave simétrica, uma par assimétrico e um PCS (não implementado) autenticado como usuário.
        Após isso, tenta ler e deletar as chaves geradas em outros papéis de acesso.
    '''

    # pega todos os mecanismos
    mechanisms = token.slot.get_mechanisms()

    # filtra os mecanismos que suportam geração de chaves/parâmetros
    mechanisms = list(filter(lambda mechanism: token.slot.get_mechanism_info(mechanism).flags in [MechanismFlag.GENERATE, MechanismFlag.GENERATE_KEY_PAIR], mechanisms))
    
    user_keys = []

    # com uma sessão de user com r/w, gera uma chave para cada mecanismo que suporta geração de chaves
    # todo: fazer o mesmo para PCS e certificados
    with token.open(rw=True, user_pin=pin) as user_session:
        for mechanism in mechanisms:
            mech_info = token.slot.get_mechanism_info(mechanism) # pega as informações do mecanismo
            try:
                # tenta gerar uma chave para o mecanismo
                if mech_info.flags == MechanismFlag.GENERATE:
                    user_keys.append(user_session.generate_key(label=f"chave{len(user_keys)}", \
                                                            store=True, mechanism=mechanism, \
                                                            id=rd.randbytes(10), \
                                                            key_length = mech_info.max_key_size))
                elif mech_info.flags == MechanismFlag.GENERATE_KEY_PAIR:
                    user_keys.append(user_session.generate_keypair(label=f"chave{len(user_keys)}", \
                                                            store=True, mechanism=mechanism, \
                                                            id=rd.randbytes(10), \
                                                            key_length = mech_info.max_key_size))
            except pkcs11.exceptions.MechanismInvalid:
                continue

    # com um sessão de SO com r/w, tenta acessar e deletar as chaves geradas
    with token.open(rw=True, so_pin=puk) as so_session:
        status = AcessDestroyKeys(user_keys, so_session)

    # com um sessãonão autenticada com r/w, tenta acessar e deletar as chaves geradas
    with token.open(rw=True) as noauth_session:
        status = AcessDestroyKeys(user_keys, noauth_session)
                
    # limpa todos os objetos criados do token
    with token.open(rw=True, user_pin=pin) as user_session:
        status = AcessDestroyKeys(user_keys, user_session)

def verifyApprovedMechanisms(token : pkcs11.Token, pin : str = "1234") -> bool:

    with token.open(user_pin=pin) as user_session:

        mechanisms = token.slot.get_mechanisms() # pega todos os mecanismos

        # filtra os mecanismos que suportam geração de chaves/parâmetros/certificados
        mechanisms = list(filter(lambda mechanism: token.slot.get_mechanism_info(mechanism).flags in [MechanismFlag.GENERATE, MechanismFlag.GENERATE_KEY_PAIR], mechanisms))

        for mechanism in mechanisms:
            if mechanism not in APPROVED_CERT_GEN_MECHANISMS or mechanism not in APPROVED_PARAM_GEN_MECHANISMS or mechanism not in APPROVED_KEY_GEN_MECHANISMS:
                return False
            
    return True

def I_11(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_15(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_31(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_40(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_41(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_42(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_46(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_48(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_53(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_54(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_55(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_56(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_57(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

def I_58(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    pass

# I.59, I.60, 61, 62, 63, 64, 65, 66, 
# II.7, 10, 15, 16
# IV.3, 4

REQUISITOS_CARTAO = {"II.7": testsAccessObjects, "II.8": testsAccessObjects, "II.11": verifyApprovedMechanisms }
REQUISITOS_TOKEN = {"I.16": testsAccessObjects, "I.26": testsAccessObjects, "I.27": testsAccessObjects, "I.34": verifyApprovedMechanisms}
'''
    END TESTS DEFINE SECTION
'''

'''
    GENERAL SECTION
'''
def ParseRequirements(requirements : list, hw_type : str) -> list:
    '''
        Recebe uma lista de requisitos e retorna uma lista de str com o nome de cada requisito.
    '''

    if hw_type.lower() == "token":
        all_requirements = REQUISITOS_TOKEN
    elif hw_type.lower() == "card":
        all_requirements = REQUISITOS_CARTAO
    else:
        raise Exception("Tipo de hardware não suportado: " + hw_type)

    if len(requirements) == 1 and requirements[-1] == "All":
        return all_requirements.keys()
    
    requirements_parsed = []

    for item in requirements:
        if item.find("-") == -1: # se não encontrar o caractere "-", adiciona
            requirements_parsed.append(item)
            continue

        requirement_interval = item.split("-")
        # só suporta intervalos de requisitos com 2 elementos (ex: II.7-II.9)
        if len(requirement_interval) < 2: # se não tiver pelo menos 2 elementos, retorna erro
            raise Exception("Requisito final não específicado no intervalo: " + item)
        
        # não suporta intervalos que comecem em um conjunto e termine em outro (ex: I.1-II.3)        
        left_set = requirement_interval[0].split(".")[0]
        right_set = requirement_interval[-1].split(".")[0]

        if left_set != right_set:
            raise Exception("Intervalo de requisitos não suportado: " + item)
        
        # caso tenha mais de 2, serão considerados o primeiro e o último elemento (ex: II.7-II.9-II.10-II.15 == II.7-II.15)
        try:
            left = int(requirement_interval[0].split(".")[-1])
            right = int(requirement_interval[-1].split(".")[-1])

            if left > right:
                left, right = right, left
        except ValueError:
            raise Exception("Requisito não numérico: " + item)
        else:
            # adiciona todos os requisitos do intervalo
            for i in range(left, right+1):
                # ignora requisitos que tenham mais de um digito (ex: II.10.1 == II.10)
                requirements_parsed.append(left_set + "." + str(i))

    # remove requisitos duplicados
    requirements_parsed = list(set(requirements_parsed))

    # verifica se todos os requisitos existem
    for requirement in requirements_parsed:
        if requirement not in all_requirements.keys():
            raise Exception("Requisito não existente: " + requirement)

    return requirements_parsed
'''
    END GENERAL SECTION
'''