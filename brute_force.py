# brute_force.py
# 第4关：暴力破解 S-DES 密钥（密钥空间 2^10 = 1024）
import time
from sdes.cipher import encrypt


def str_to_bits(s):
    return [int(c) for c in s]


def bits_to_str(bits):
    return ''.join(str(b) for b in bits)


def brute_force(plain_bits, cipher_bits):
    """
    遍历所有 1024 个可能的 10-bit 密钥，
    找出能加密出指定密文的密钥（可能不止一个）。
    """
    found = []
    for k in range(1024):
        key_bits = [int(b) for b in format(k, '010b')]
        if encrypt(plain_bits, key_bits) == cipher_bits:
            found.append(bits_to_str(key_bits))
    return found


if __name__ == "__main__":
    print("=== S-DES 暴力破解 ===")
    pt = input("请输入 8-bit 明文 (如 10111101): ").strip()
    real_key = input("请输入 10-bit 密钥 (如 1010000010): ").strip()

    pt_bits = str_to_bits(pt)
    key_bits = str_to_bits(real_key)

    # 用真实密钥加密，得到明密文对
    ct_bits = encrypt(pt_bits, key_bits)
    ct = bits_to_str(ct_bits)
    print(f"\n加密结果: 明文 {pt} + 密钥 {real_key} -> 密文 {ct}")

    # 暴力破解并计时
    start = time.time()
    found_keys = brute_force(pt_bits, ct_bits)
    elapsed = time.time() - start

    print(f"\n暴力破解耗时: {elapsed * 1000:.2f} 毫秒")
    print(f"找到 {len(found_keys)} 个能加密出该密文的密钥:")
    for key in found_keys:
        print(f"  {key}")

    if real_key in found_keys:
        print(f"\n原始密钥 {real_key} 在结果中 ✅")
    else:
        print(f"\n原始密钥 {real_key} 不在结果中 ❌")