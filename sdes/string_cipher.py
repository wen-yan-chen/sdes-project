# sdes/string_cipher.py
# 第3关：把 S-DES 应用到 ASCII 字符串
from .cipher import encrypt, decrypt


def encrypt_string(text, key_bits):
    """
    将字符串按 ASCII 逐字符加密。
    每个字符转成 8-bit，用 S-DES 加密，再把结果拼成一个二进制字符串返回。
    """
    cipher_bits = []
    for char in text:
        byte = ord(char)                              # 获取 ASCII 码
        bits = [int(b) for b in format(byte, '08b')]  # 转成 8-bit 列表
        enc = encrypt(bits, key_bits)
        cipher_bits.extend(enc)
    return ''.join(str(b) for b in cipher_bits)


def decrypt_string(binary_str, key_bits):
    """
    将二进制密文串按 8-bit 分组解密回字符串。
    """
    result = []
    for i in range(0, len(binary_str), 8):
        bits = [int(b) for b in binary_str[i:i + 8]]
        dec = decrypt(bits, key_bits)
        byte = int(''.join(str(b) for b in dec), 2)
        result.append(chr(byte))
    return ''.join(result)