# test_run.py
from sdes.cipher import encrypt, decrypt


def str_to_bits(s):
    return [int(c) for c in s]


def bits_to_str(bits):
    return ''.join(str(b) for b in bits)


# 标准测试向量
key = str_to_bits("1010000010")
pt  = str_to_bits("10111101")

ct = encrypt(pt, key)
print("明文:", bits_to_str(pt))
print("密文:", bits_to_str(ct))

pt2 = decrypt(ct, key)
print("解密:", bits_to_str(pt2))

# 自检：加密再解密应还原
if pt2 == pt:
    print("✅ 自洽性通过")
else:
    print("❌ 出错")