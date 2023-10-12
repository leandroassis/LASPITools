from pkcs11.mechanisms import Mechanism
from pkcs11.mechanisms import KeyType

'''
    MECHANISM SECTION
'''
APPROVED_MECHANISMS = {
    Mechanism.RSA_PKCS_KEY_PAIR_GEN:KeyType.RSA,
    Mechanism.DSA_KEY_PAIR_GEN:KeyType.DSA,
    Mechanism.DH_PKCS_KEY_PAIR_GEN:KeyType.DH,
    Mechanism.DES2_KEY_GEN:KeyType.DES2,
    Mechanism.DES3_KEY_GEN:KeyType.DES3,
    Mechanism.EC_KEY_PAIR_GEN:KeyType.EC,
    Mechanism.AES_KEY_GEN:KeyType.AES,
    Mechanism.EC_EDWARDS_KEY_PAIR_GEN:KeyType.EC_EDWARDS,
    Mechanism._DES_KEY_GEN:KeyType.DES3,
}
'''
    END MECHANISM SECTION
'''

'''
    GENERAL SECTION
'''
# configurações de print
COLUMN_WIDTH = 55
COLUMN_SEPARATOR = "="
END_SECTION_LINE = "\n"+COLUMN_SEPARATOR*COLUMN_WIDTH+"\n"

REQS_POR_LINHA = 8

# configurações do mutex
SLEEP_THREAD_TIME = 0.4 # segundos
'''
    END GENERAL SECTION
'''


