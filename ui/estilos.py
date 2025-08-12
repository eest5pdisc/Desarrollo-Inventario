import tkinter as tk
from tkinter import ttk

def configurar_estilos():
    style = ttk.Style()
    style.theme_use("clam")
    # ...todas las llamadas a style.configure y style.map...
    
    # --- Configuración de Estilos (Diseño Gráfico) ---
    style = ttk.Style()
    style.theme_use("clam")

    # Estilo para los botones del menú lateral
    style.configure("Menu.TButton",
                    background="#34495E",
                    foreground="white",
                    font=("Arial", 10, "bold"),
                    relief="flat",
                    padding=[10, 5])
    style.map("Menu.TButton",
            background=[('active', '#2C3E50')])

    # Estilo para Treeview (tabla)
    style.configure("Treeview.Heading",
                    font=("Arial", 10, "bold"),
                    background="#DDEEFF",
                    foreground="#333333",
                    padding=[5, 5])
    style.configure("Treeview",
                    font=("Arial", 9),
                    rowheight=25,
                    background="white",
                    foreground="#333333",
                    fieldbackground="white")
    style.map("Treeview",
            background=[('selected', '#3498DB')],
            foreground=[('selected', 'white')])

    # Estilo para Entry (campos de texto) y Combobox, Spinbox
    style.configure("TEntry", font=("Arial", 9), padding=5)
    style.configure("TCombobox", font=("Arial", 9), padding=5)
    style.configure("TSpinbox", font=("Arial", 9), padding=5)

    # Estilo para Labels dentro de los frames de contenido (blancos)
    style.configure("TLabel", background="white", font=("Arial", 9))
    style.configure("TButton", font=("Arial", 10, "bold"))

    # NUEVOS ESTILOS PARA BOTONES DE ACCIÓN ESPECÍFICOS
    # Estilo para el botón de eliminar (rojo)
    style.configure("Danger.TButton",
                    background="#E74C3C",
                    foreground="white",
                    font=("Arial", 10, "bold"),
                    relief="flat",
                    padding=[10, 5])
    style.map("Danger.TButton",
            background=[('active', '#C0392B')])

    # Estilo para el botón de actualizar o primario (azul)
    style.configure("Primary.TButton",
                    background="#2980B9",
                    foreground="white",
                    font=("Arial", 10, "bold"),
                    relief="flat",
                    padding=[10, 5])
    style.map("Primary.TButton",
            background=[('active', '#2471A3')])

    # Estilo para el botón de devolución (verde)
    style.configure("Success.TButton",
                    background="#27AE60", # Verde
                    foreground="white",
                    font=("Arial", 10, "bold"),
                    relief="flat",
                    padding=[10, 5])
    style.map("Success.TButton",
            background=[('active', '#229954')])

    # Nuevos estilos para tags de Treeview
    style.configure("Treeview.tag_vencido", background="#FADBD8", foreground="#C0392B", font=("Arial", 9, "bold")) # Rojo claro, texto rojo
    style.configure("Treeview.tag_devuelto", background="#EAF2F8", foreground="#5D6D7E") # Azul claro grisáceo


    # ...líneas 8 a 61 del archivo original...
    return style