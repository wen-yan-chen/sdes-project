# collision_test.py
# 第5关：封闭测试，分析密钥碰撞
from collections import Counter
from sdes.cipher import encrypt


def str_to_bits(s):
    return [int(c) for c in s]


def bits_to_str(bits):
    return ''.join(str(b) for b in bits)


if __name__ == "__main__":
    plaintext = "10111101"
    pt_bits = str_to_bits(plaintext)

    # 统计：每个密文对应多少个密钥
    cipher_map = {}  # 密文 -> 能生成它的密钥列表

    for k in range(1024):
        key_bits = [int(b) for b in format(k, '010b')]
        ct = bits_to_str(encrypt(pt_bits, key_bits))
        cipher_map.setdefault(ct, []).append(bits_to_str(key_bits))

    print(f"明文: {plaintext}")
    print(f"总密钥数: 1024")
    print(f"不同密文数: {len(cipher_map)}")

    # 统计每个密文对应几个密钥
    counts = Counter(len(keys) for keys in cipher_map.values())
    print("\n密钥数量分布:")
    for num_keys, count in sorted(counts.items()):
        print(f"  一个密文对应 {num_keys} 个密钥: 共有 {count} 个这样的密文")

    # 具体示例：显示前 3 个密钥碰撞的密文
    print("\n密钥碰撞示例 (前 3 个):")
    shown = 0
    for ct, keys in cipher_map.items():
        if len(keys) > 1:
            print(f"  密文 {ct} 可由 {len(keys)} 个密钥生成:")
            for key in keys:
                print(f"      {key}")
            shown += 1
            if shown >= 3:
                break