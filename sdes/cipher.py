# sdes/cipher.py
from .core import *


def encrypt(plain_bits, key_bits):
    """加密：IP → fk1 → SW → fk2 → IP⁻¹"""
    k1, k2 = key_expansion(key_bits)

    ip  = permute(plain_bits, IP)
    fk1 = fk(ip, k1)
    sw  = swap(fk1)
    fk2 = fk(sw, k2)
    return permute(fk2, IP_INV)


def decrypt(cipher_bits, key_bits):
    """解密：子密钥顺序反过来，先 K2 后 K1"""
    k1, k2 = key_expansion(key_bits)

    ip  = permute(cipher_bits, IP)
    fk1 = fk(ip, k2)          # 注意：解密先用 K2
    sw  = swap(fk1)
    fk2 = fk(sw, k1)          # 再用 K1
    return permute(fk2, IP_INV)