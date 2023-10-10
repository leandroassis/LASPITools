from pkcs11.mechanisms import Mechanism

# todo: remover todos os mecanismos que não fazem sentido no contexto das certificações
APPROVED_KEY_GEN_MECHANISMS = [
    Mechanism.RSA_PKCS_KEY_PAIR_GEN,
    Mechanism.RSA_X9_31_KEY_PAIR_GEN,
    Mechanism.DSA_KEY_PAIR_GEN,
    Mechanism.DH_PKCS_KEY_PAIR_GEN,
    Mechanism.X9_42_DH_KEY_PAIR_GEN,
    Mechanism.DES2_KEY_GEN,
    Mechanism.DES3_KEY_GEN,
    Mechanism.SECURID_KEY_GEN,
    Mechanism.HOTP_KEY_GEN,
    Mechanism.ACTI_KEY_GEN,
    Mechanism.GENERIC_SECRET_KEY_GEN,
    Mechanism.SSL3_PRE_MASTER_KEY_GEN,
    Mechanism.TLS_PRE_MASTER_KEY_GEN,
    Mechanism.WTLS_PRE_MASTER_KEY_GEN,
    Mechanism.SEED_KEY_GEN,
    Mechanism.EC_KEY_PAIR_GEN,
    Mechanism.AES_KEY_GEN,
    Mechanism.BLOWFISH_KEY_GEN,
    Mechanism.TWOFISH_KEY_GEN,
    Mechanism.GOSTR3410_KEY_PAIR_GEN,
    Mechanism.GOST28147_KEY_GEN,
    Mechanism.EC_EDWARDS_KEY_PAIR_GEN
]

APPROVED_CERT_GEN_MECHANISMS = [

]

APPROVED_PARAM_GEN_MECHANISMS = [
    Mechanism.DSA_PARAMETER_GEN,
    Mechanism.DH_PKCS_PARAMETER_GEN,
    Mechanism.X9_42_DH_PARAMETER_GEN
]