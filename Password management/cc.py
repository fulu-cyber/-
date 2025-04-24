import tkinter as tk
from tkinter import ttk, messagebox
import json
import secrets
import string
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class PasswordManager:
    def __init__(self, key_path='key.bin', data_path='data.enc'):
        self.root = tk.Tk()
        self.key_path = key_path
        self.data_path = data_path
        self.root.title("安全密码管理器")
        
        # 初始化UI组件
        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        # 密码输入框
# 推测你想将“保存”功能改为“查询”功能，以下是对界面部分的修改，添加查询按钮和查询输入框
        ttk.Label(self.root, text="站点/应用名称:").grid(row=0, column=0, padx=5, pady=5)
        self.site_entry = ttk.Entry(self.root, width=30)
        self.site_entry.grid(row=0, column=1, padx=5, pady=5)

        # 保存按钮
        ttk.Button(self.root, text="保存记录", command=self.save_entry).grid(row=2, column=0, columnspan=2, pady=10)

        # 历史记录表格
        self.tree = ttk.Treeview(self.root, columns=('Site', 'Password', 'Notes'), show='headings')
        self.tree.heading('Site', text='站点')
        self.tree.heading('Password', text='密码')
        self.tree.heading('Notes', text='备注')
        self.tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.tree.bind('<Double-1>', self.on_double_click)


    def encrypt_data(self, data):
        nonce = secrets.token_bytes(12)
        cipher = AES.new(self.encryption_key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(pad(data.encode(), AES.block_size))
        return base64.b64encode(nonce + tag + ciphertext).decode()

    def decrypt_data(self, encrypted_data):
        data = base64.b64decode(encrypted_data)
        nonce, tag, ciphertext = data[:12], data[12:28], data[28:]
        cipher = AES.new(self.encryption_key, AES.MODE_GCM, nonce=nonce)
        return unpad(cipher.decrypt_and_verify(ciphertext, tag), AES.block_size).decode()

    def load_config(self):
        try:
            # 加载或生成加密密钥
            if os.path.exists('key.bin'):
                with open('key.bin', 'rb') as f:
                    self.encryption_key = f.read()
            else:
                self.encryption_key = secrets.token_bytes(32)
                with open('key.bin', 'wb') as f:
                    f.write(self.encryption_key)
            
            # 加载已有数据
            if os.path.exists('data.enc'):
                with open('data.enc', 'r') as f:
                    for line in f:
                        entry = json.loads(line.strip())
                        decrypted_pwd = self.decrypt_data(entry['password'])
                        self.tree.insert('', 'end', 
                            values=(entry['site'], '******', entry['notes']))
        except Exception as e:
            messagebox.showerror("错误", f"配置加载失败: {str(e)}")

    def save_entry(self, site, password, notes):
        if not all([site, password]):
            raise ValueError("站点和密码不能为空")
        try:
            entry_data = json.dumps({
                'site': site,
                'password': self.encrypt_data(password),
                'notes': notes
            })
            with open(self.data_path, 'a') as f:
                f.write(entry_data + '\n')
        except Exception as e:
            raise RuntimeError(f"加密保存失败: {str(e)}")

    def refresh_data(self):
        self.tree.delete(*self.tree.get_children())
        self.load_config()

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        site = self.tree.item(item, 'values')[0]
        
        with open('data.enc', 'r') as f:
            for line in f:
                entry = json.loads(line.strip())
                if entry['site'] == site:
                    decrypted_pwd = self.decrypt_data(entry['password'])
                    messagebox.showinfo('解密密码', f'站点：{site}\n密码：{decrypted_pwd}')
                    break

if __name__ == "__main__":
    app = PasswordManager()
    app.root.mainloop()