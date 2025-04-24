import tkinter as tk

from tkinter import ttk, messagebox

import secrets

import string

import pyperclip



class PasswordGenerator:

    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("安全密码生成器")
        self.master.geometry("680x500")
        self.master.resizable(False, False)



        # 控件变量初始化

        self.length_var = tk.StringVar(value="12")

        self.upper_var = tk.BooleanVar(value=True)

        self.lower_var = tk.BooleanVar(value=True)

        self.digits_var = tk.BooleanVar(value=True)

        self.symbols_var = tk.BooleanVar(value=True)

        self.password_var = tk.StringVar()



        # 界面布局

        self.create_widgets()



    def create_widgets(self):
        """构建图形界面"""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('微软雅黑', 10))
        style.configure('TButton', font=('微软雅黑', 10), width=12)
        style.configure('TCheckbutton', background='#f0f0f0')

        # 主容器
        main_frame = ttk.Frame(self.master, padding=20)
        main_frame.pack(fill='both', expand=True)

        # 输入区域
        input_frame = ttk.LabelFrame(main_frame, text=" 密码信息 ", padding=15)
        input_frame.grid(row=0, column=0, pady=10, sticky="ew")

        ttk.Label(input_frame, text="站点/应用名称：").grid(row=0, column=0, sticky="w")
        self.site_entry = ttk.Entry(input_frame, width=28)
        self.site_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="备　　注：").grid(row=1, column=0, sticky="w")
        self.notes_entry = ttk.Entry(input_frame, width=28)
        self.notes_entry.grid(row=1, column=1, padx=5, pady=5)

        # 选项区域
        option_frame = ttk.LabelFrame(main_frame, text=" 字符选项 ", padding=15)
        option_frame.grid(row=1, column=0, pady=10, sticky="ew")

        ttk.Label(option_frame, text="密码长度：").grid(row=0, column=0, sticky="w")
        ttk.Entry(option_frame, textvariable=self.length_var, width=5).grid(row=0, column=1, sticky="w")

        check_buttons = [
            ("大写字母(A-Z)", self.upper_var),
            ("小写字母(a-z)", self.lower_var),
            ("数字(0-9)", self.digits_var),
            ("符号(!@#$)", self.symbols_var)
        ]
        
        for i, (text, var) in enumerate(check_buttons):
            ttk.Checkbutton(option_frame, text=text, variable=var).grid(row=i+1, column=0, columnspan=2, sticky="w", pady=2)

        # 操作按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=15)

        ttk.Button(button_frame, text="生成密码", command=self.generate_password).grid(row=0, column=0, padx=5)

        # 结果显示区域
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=3, column=0, sticky="ew", pady=10)

        ttk.Label(result_frame, text="生成结果：").grid(row=0, column=0, sticky="w")
        result_entry = ttk.Entry(result_frame, textvariable=self.password_var, state="readonly", width=25)
        result_entry.grid(row=0, column=1, padx=5)
        ttk.Button(result_frame, text="复制密码", command=self.copy_password).grid(row=0, column=2, padx=5)
        ttk.Button(result_frame, text="保存密码", command=self.save_password).grid(row=0, column=3, padx=5)



    def generate_password(self):

        """核心生成逻辑"""

        try:

            # 参数校验

            length = int(self.length_var.get())

            charset = self.build_charset()



            # 安全检测

            if not charset:

                raise ValueError("请至少选择一种字符类型")

            if length < 8:

                messagebox.showwarning("安全警告", "密码长度建议≥8位！")



            # 密码生成

            password = ''.join(secrets.choice(charset) for _ in range(length))

            self.password_var.set(password)

            pyperclip.copy(password)  # 自动复制到剪贴板



        except ValueError as e:

            messagebox.showerror("参数错误", f"输入无效：{str(e)}")

        except Exception as e:

            messagebox.showerror("系统错误", f"生成失败：{str(e)}")



    def build_charset(self):

        """构建字符集"""

        charset = ""

        if self.upper_var.get(): charset += string.ascii_uppercase

        if self.lower_var.get(): charset += string.ascii_lowercase 

        if self.digits_var.get(): charset += string.digits

        if self.symbols_var.get(): charset += string.punctuation

        return charset



    def save_password(self):
        """保存密码逻辑"""
        site = self.site_entry.get()
        notes = self.notes_entry.get()
        password = self.password_var.get()

        if not all([site, password]):
            messagebox.showerror("错误", "站点名称和密码不能为空")
            return

        try:
            from cc import PasswordManager
            manager = PasswordManager('key.bin', 'data.enc')
            manager.save_entry(site, password, notes)
            messagebox.showinfo("成功", "密码已加密存储")
            manager.refresh_data()
        except Exception as e:
            error_detail = str(e)
            if "加密" in error_detail:
                messagebox.showerror("加密失败", f"加密过程中出错：{error_detail}")
            elif "文件" in error_detail:
                messagebox.showerror("存储失败", f"文件读写错误：{error_detail}")
            else:
                messagebox.showerror("存储失败", f"系统错误：{error_detail}")

    def copy_password(self):

        """复制到剪贴板"""

        if self.password_var.get():

            pyperclip.copy(self.password_var.get())

            messagebox.showinfo("操作成功", "密码已复制到剪贴板")



if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()