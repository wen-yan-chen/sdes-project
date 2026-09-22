\# S-DES 接口文档



本文档描述 S-DES 项目中各模块对外提供的核心接口，供二次开发或集成使用。



\---



\## 一、模块层级



```

gui.py / brute\_force.py / collision\_test.py   （应用层）

&#x20;           ↓

sdes.string\_cipher                             （字符串接口）

&#x20;           ↓

sdes.cipher                                    （加解密主流程）

&#x20;           ↓

sdes.core                                      （密钥扩展、轮函数）

&#x20;           ↓

sdes.constants                                 （参数表）

```



调用方只需依赖 `sdes.cipher` 和 `sdes.string\_cipher` 两层，即可完成所有功能。



\---



\## 二、数据结构约定



所有 bit 序列在内部统一用 \*\*Python list\*\* 表示，每个元素是整数 `0` 或 `1`。



例如 8-bit 明文 `10111101` 表示为：



```python

\[1, 0, 1, 1, 1, 1, 0, 1]

```



\*\*长度约定\*\*：



| 数据 | 长度 |

|------|------|

| 明文 / 密文 | 8 |

| 密钥 | 10 |

| 子密钥 K1 / K2 | 8 |



\---



\## 三、核心接口



\### 1. `sdes.cipher.encrypt(plain\_bits, key\_bits) -> list`



对单个 8-bit 分组进行加密。



\- \*\*参数\*\*：

&#x20; - `plain\_bits`：8 位明文列表，如 `\[1,0,1,1,1,1,0,1]`

&#x20; - `key\_bits`：10 位密钥列表，如 `\[1,0,1,0,0,0,0,0,1,0]`

\- \*\*返回值\*\*：8 位密文列表

\- \*\*流程\*\*：`IP → fk1 → SW → fk2 → IP⁻¹`

\- \*\*示例\*\*：



```python

from sdes.cipher import encrypt



pt  = \[1,0,1,1,1,1,0,1]

key = \[1,0,1,0,0,0,0,0,1,0]

ct  = encrypt(pt, key)

\# ct = \[1,1,0,0,0,0,1,1]

```



\---



\### 2. `sdes.cipher.decrypt(cipher\_bits, key\_bits) -> list`



对单个 8-bit 分组进行解密，是 `encrypt` 的逆运算。



\- \*\*参数\*\*：

&#x20; - `cipher\_bits`：8 位密文列表

&#x20; - `key\_bits`：10 位密钥列表（\*\*与加密使用同一密钥\*\*）

\- \*\*返回值\*\*：8 位明文列表

\- \*\*说明\*\*：解密时子密钥使用顺序与加密相反（先 K2 后 K1）

\- \*\*示例\*\*：



```python

from sdes.cipher import decrypt



ct = \[1,1,0,0,0,0,1,1]

key = \[1,0,1,0,0,0,0,0,1,0]

pt = decrypt(ct, key)

\# pt = \[1,0,1,1,1,1,0,1]

```



\---



\### 3. `sdes.string\_cipher.encrypt\_string(text, key\_bits) -> str`



对任意字符串进行加密，按 ASCII 逐字节处理。



\- \*\*参数\*\*：

&#x20; - `text`：任意 ASCII 字符串，如 `"This is a pen"`

&#x20; - `key\_bits`：10 位密钥列表

\- \*\*返回值\*\*：二进制密文字符串，长度 = `len(text) \* 8`

\- \*\*说明\*\*：每个字符先转成 8-bit ASCII，再用 `encrypt` 加密，结果拼接

\- \*\*示例\*\*：



```python

from sdes.string\_cipher import encrypt\_string



key = \[1,0,1,0,0,0,0,0,1,0]

ct  = encrypt\_string("abc", key)

\# ct 是一个 24 位的二进制字符串

```



\---



\### 4. `sdes.string\_cipher.decrypt\_string(binary\_str, key\_bits) -> str`



对二进制密文串进行解密，还原字符串。



\- \*\*参数\*\*：

&#x20; - `binary\_str`：长度是 8 的倍数的二进制字符串

&#x20; - `key\_bits`：10 位密钥列表（与加密一致）

\- \*\*返回值\*\*：解密后的字符串

\- \*\*示例\*\*：



```python

from sdes.string\_cipher import decrypt\_string



key = \[1,0,1,0,0,0,0,0,1,0]

pt  = decrypt\_string(ct, key)

\# pt = "abc"

```



\---



\### 5. `sdes.core.key\_expansion(key\_10) -> (k1, k2)`



对 10-bit 主密钥进行扩展，生成两个 8-bit 子密钥。



\- \*\*参数\*\*：

&#x20; - `key\_10`：10 位密钥列表

\- \*\*返回值\*\*：元组 `(k1, k2)`，两个 8 位列表

\- \*\*流程\*\*：`P10 → 分左右 5 位 → 左移 1 位 → P8` 得 K1；`P10 → 分左右 → 左移 2 位 → P8` 得 K2

\- \*\*示例\*\*：



```python

from sdes.core import key\_expansion



key = \[1,0,1,0,0,0,0,0,1,0]

k1, k2 = key\_expansion(key)

\# k1 和 k2 各为 8 位列表

```



\---



\## 四、内部工具函数（供调试使用）



以下函数位于 `sdes.core` 中，一般不直接对外暴露，但理解它们有助于调试：



| 函数 | 作用 |

|------|------|

| `permute(bits, table)` | 通用置换：按 `table` 的索引顺序重排 bit |

| `left\_shift(bits, positions)` | 按位置列表做循环左移 |

| `xor(a, b)` | 两个等长 bit 列表逐位异或 |

| `sbox\_lookup(bits\_4, sbox)` | 4-bit 输入查 4×4 S-box，返回 2-bit |

| `round\_function(right\_4, subkey\_8)` | 轮函数 F |

| `fk(bits\_8, subkey\_8)` | Feistel 的一轮 |

| `swap(bits\_8)` | 交换左右 4 位 |



\---



\## 五、异常与边界说明



\- 所有列表参数长度必须严格匹配（明文 8、密钥 10），否则结果无意义。

\- `string\_cipher` 只支持 ASCII 字符（`ord(c) <= 255`）。若传入非 ASCII 字符（如中文），会因超出 8-bit 而报错。

\- `brute\_force`、`collision\_test` 等脚本依赖 `sdes.cipher`，不对外暴露接口，仅作演示。



\---



\## 六、调用示例（完整流程）



```python

from sdes.cipher import encrypt, decrypt

from sdes.string\_cipher import encrypt\_string, decrypt\_string



def str\_to\_bits(s):

&#x20;   return \[int(c) for c in s]



def bits\_to\_str(bits):

&#x20;   return ''.join(str(b) for b in bits)



key = str\_to\_bits("1010000010")



\# --- 8-bit 加解密 ---

pt = str\_to\_bits("10111101")

ct = encrypt(pt, key)

print("密文:", bits\_to\_str(ct))       # 11000011



pt2 = decrypt(ct, key)

print("还原:", bits\_to\_str(pt2))      # 10111101



\# --- 字符串加解密 ---

ct\_str = encrypt\_string("Hello", key)

print("字符串密文长度:", len(ct\_str))  # 40



pt\_str = decrypt\_string(ct\_str, key)

print("字符串还原:", pt\_str)          # Hello

```

