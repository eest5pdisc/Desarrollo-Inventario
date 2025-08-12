from db import funciones as db
from ui.login import LoginApp

if __name__ == "__main__":
    db.crear_tablas()
    if not db.verificar_credenciales_db("admin", "adminpass"):
        db.registrar_usuario_db("admin", "adminpass", "admin")
    if not db.verificar_credenciales_db("usuario", "userpass"):
        db.registrar_usuario_db("usuario", "userpass", "usuario")
    login_window = LoginApp()
    login_window.mainloop()