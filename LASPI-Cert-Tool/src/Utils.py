import pkcs11
from pkcs11.constants import MechanismFlag, ObjectClass
import random as rd



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
                # captura o erro ao não conseguir destruir a chave
                print(e)
                continue
            else:
                # se acessar a chave e não for lançada nenhuma exceção, retorna False caso a chave não seja pública
                if key.object_class != ObjectClass.PUBLIC_KEY:
                    return False

    return True

def MCII_7(token : pkcs11.Token, pin : str = "1234", puk : str = "12345678") -> bool:
    '''
        Gera uma chave simétrica, uma chave assimétrica privada e um PCS (não implementado) autenticado como usuário.
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
        

    

    
