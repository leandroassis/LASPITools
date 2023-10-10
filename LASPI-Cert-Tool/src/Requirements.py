import pkcs11
from pkcs11.constants import MechanismFlag
from pkcs11.mechanisms import Mechanism
import random as rd

from defines import APPROVED_KEY_GEN_MECHANISMS, APPROVED_CERT_GEN_MECHANISMS, APPROVED_PARAM_GEN_MECHANISMS
from Utils import AcessDestroyKeys

# TO DO: ADICIONAR INFORMAÇÕES DE LOG EM TODOS AS FUNÇÕES


# REQUISITO MC II.7 (cartão) e I.16, I.26, I.27 (token)
def MCII_7_E_8(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
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


# I.34 (token)
def MCII_11(token : pkcs11.Token, pin : str = "1234") -> bool:

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