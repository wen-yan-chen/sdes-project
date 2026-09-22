# sdes/core.py
from .constants import *


def permute(bits, table):
    """
    通用置换函数。
    bits:  输入的 bit 列表，例如 [1, 0, 1, 1, 1, 1, 0, 1]
    table: 置换表，例如 [2, 6, 3, 1, ...]
    返回:  按 table 取出的新 bit 列表
    """
    return [bits[i - 1] for i in table]      # 注意 table 里的数字是 1-based


def left_shift(bits, positions):
    """
    按 positions 指定的顺序重排 bit，实现循环左移的效果。
    例如 positions = [2,3,4,5,1] 表示把原来的第2位放到第1位...
    """
    return [bits[i - 1] for i in positions]


def xor(bits_a, bits_b):
    """两个等长 bit 列表逐位异或"""
    return [a ^ b for a, b in zip(bits_a, bits_b)]


def sbox_lookup(bits_4, sbox):
    """
    4-bit 输入查 4x4 S-box。
    行号 = 第1位和第4位拼成的二进制
    列号 = 第2位和第3位拼成的二进制
    返回 2-bit 列表
    """
    row = bits_4[0] * 2 + bits_4[3]
    col = bits_4[1] * 2 + bits_4[2]
    val = sbox[row][col]
    return [(val >> 1) & 1, val & 1]

def key_expansion(key_10):
    """
    输入 10-bit 密钥（list），返回 K1、K2 两个 8-bit 子密钥。
    流程: P10 → 分左右 → 各左移1位 → P8 得 K1
                     → 各左移2位 → P8 得 K2
    """
    p10_key = permute(key_10, P10)
    left, right = p10_key[:5], p10_key[5:]

    # 生成 K1
    ls1_left  = left_shift(left, LS1)
    ls1_right = left_shift(right, LS1)
    k1 = permute(ls1_left + ls1_right, P8)

    # 生成 K2
    ls2_left  = left_shift(left, LS2)
    ls2_right = left_shift(right, LS2)
    k2 = permute(ls2_left + ls2_right, P8)

    return k1, k2

def round_function(right_4, subkey_8):
    """
    轮函数 F：
    4-bit 右半 + 8-bit 子密钥 → E/P 扩展 → 异或 → S-box → SP 置换 → 4-bit
    """
    expanded = permute(right_4, EPBOX)      # 扩成 8-bit
    xored    = xor(expanded, subkey_8)      # 与子密钥异或

    left_4, right_4 = xored[:4], xored[4:]
    s1_out = sbox_lookup(left_4, SBOX1)     # 2-bit
    s2_out = sbox_lookup(right_4, SBOX2)    # 2-bit
    combined = s1_out + s2_out              # 4-bit

    return permute(combined, SPBOX)         # SP 置换后输出 4-bit


def fk(bits_8, subkey_8):
    """
    Feistel 的一轮：左边 4 位 XOR F(右边4位, 子密钥)，右边不变。
    """
    left, right = bits_8[:4], bits_8[4:]
    f_out = round_function(right, subkey_8)
    new_left = xor(left, f_out)
    return new_left + right


def swap(bits_8):
    """SW：把 8-bit 数据的左右 4 位对调"""
    return bits_8[4:] + bits_8[:4]