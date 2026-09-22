# gui.py
# 第1关 + 第3关：S-DES 加解密 GUI（8-bit 二进制 + ASCII 字符串）
import tkinter as tk
from tkinter import messagebox
from sdes.cipher import encrypt, decrypt
from sdes.string_cipher import encrypt_string, decrypt_string


def str_to_bits(s):
    return [int(c) for c in s]


def bits_to_str(bits):
    return ''.join(str(b) for b in bits)


def validate(bits_str, length, name):
    if len(bits_str) != length:
        raise ValueError(f"{name} 必须是 {length} 位")
    if any(c not in '01' for c in bits_str):
        raise ValueError(f"{name} 只能包含 0 和 1")


def get_key_bits():
    key = key_var.get().strip()
    validate(key, 10, "密钥")
    return str_to_bits(key)


def show_result(text):
    """把结果写进多行文本框"""
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, text)


def on_encrypt():
    try:
        key_bits = get_key_bits()
        if mode_var.get() == "8-bit":
            pt = input_var.get().strip()
            validate(pt, 8, "明文")
            ct = encrypt(str_to_bits(pt), key_bits)
            show_result(bits_to_str(ct))
        else:
            text = input_var.get()
            show_result(encrypt_string(text, key_bits))
    except Exception as e:
        messagebox.showerror("输入错误", str(e))


def on_decrypt():
    try:
        key_bits = get_key_bits()
        if mode_var.get() == "8-bit":
            ct = input_var.get().strip()
            validate(ct, 8, "密文")
            pt = decrypt(str_to_bits(ct), key_bits)
            show_result(bits_to_str(pt))
        else:
            binary_str = input_var.get().strip()
            show_result(decrypt_string(binary_str, key_bits))
    except Exception as e:
        messagebox.showerror("输入错误", str(e))


# ---------- 界面 ----------
root = tk.Tk()
root.title("S-DES 加解密 - 第1&3关")
root.geometry("620x500")

mode_var = tk.StringVar(value="8-bit")
tk.Label(root, text="模式:").pack(pady=(15, 5))
tk.Radiobutton(root, text="8-bit 二进制", variable=mode_var, value="8-bit").pack()
tk.Radiobutton(root, text="ASCII 字符串", variable=mode_var, value="string").pack()

input_var = tk.StringVar(value="10111101")
key_var = tk.StringVar(value="1010000010")

tk.Label(root, text="输入 (明文/密文 或 字符串):").pack(pady=(10, 5))
tk.Entry(root, textvariable=input_var, width=60, justify="center").pack()

tk.Label(root, text="密钥 (10-bit):").pack(pady=(10, 5))
tk.Entry(root, textvariable=key_var, width=40, justify="center").pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)
tk.Button(btn_frame, text="加密", width=12, command=on_encrypt).pack(side="left", padx=12)
tk.Button(btn_frame, text="解密", width=12, command=on_decrypt).pack(side="left", padx=12)

tk.Label(root, text="结果:").pack()
result_text = tk.Text(root, width=70, height=7, wrap="char")
result_text.pack(pady=5)

root.mainloop()