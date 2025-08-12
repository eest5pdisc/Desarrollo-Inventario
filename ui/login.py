import tkinter as tk
from tkinter import ttk, messagebox
from db import funciones as db
from ui.ventanas import MainApplication

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Iniciar Sesión - Sistema de Inventario")
        self.geometry("400x250")
        self.resizable(False, False)
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f'+{x}+{y}')
        self.create_widgets()

    def create_widgets(self):
        login_frame = ttk.Frame(self, padding="20")
        login_frame.pack(expand=True)
        ttk.Label(login_frame, text="Inicio de Sesión", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(login_frame, text="Usuario:").pack(anchor="w", pady=(10, 0))
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.pack(pady=5)
        self.username_entry.focus_set()
        ttk.Label(login_frame, text="Contraseña:").pack(anchor="w", pady=(10, 0))
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.pack(pady=5)
        self.password_entry.bind("<Return>", lambda event=None: self.attempt_login())
        ttk.Button(login_frame, text="Iniciar Sesión", command=self.attempt_login).pack(pady=20)

    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Campos vacíos", "Por favor, ingrese usuario y contraseña.", parent=self)
            return
        if db.verificar_credenciales_db(username, password):
            messagebox.showinfo("Éxito", "¡Sesión iniciada correctamente!", parent=self)
            self.withdraw()  # Oculta la ventana de login
            main_app = MainApplication(self)  # Usa la instancia actual como master
            main_app.wait_window()  # Espera a que la ventana principal se cierre
            self.destroy()  # Cierra la ventana de login al salir de la principal
        else:
            messagebox.showerror("Error de Logeo", "Usuario o contraseña incorrectos.", parent=self)
            self.password_entry.delete(0, tk.END)
# ...existing code...