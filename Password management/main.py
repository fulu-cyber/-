import tkinter as tk
from tkinter import ttk
from cc import PasswordManager
from sc import PasswordGenerator

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('密码管理系统')
        self.root.geometry('350x200')
        self.create_interface()

    def create_interface(self):
        ttk.Button(self.root, 
                 text='密码管理器', 
                 command=self.open_password_manager,
                 width=20).pack(pady=15)
        
        ttk.Button(self.root,
                 text='密码生成器',
                 command=self.open_password_generator,
                 width=20).pack(pady=15)

    def open_password_manager(self):
        PasswordManager(self.root)

    def open_password_generator(self):
        PasswordGenerator(self.root)

if __name__ == "__main__":
    app = MainApplication()
    app.root.mainloop()