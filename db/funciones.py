import sqlite3
import bcrypt
from datetime import datetime

DATABASE_NAME = "inventario.db"

def conectar_db():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            tipo TEXT NOT NULL,
            detalle TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_producto TEXT NOT NULL,
            solicitante TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            fecha_devolucion_esperada TEXT NOT NULL,
            fecha_devolucion_real TEXT,
            estado TEXT NOT NULL,
            FOREIGN KEY (codigo_producto) REFERENCES productos(codigo)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'usuario'
        )
    ''')
    conn.commit()
    conn.close()

# --- Productos ---
def agregar_producto_db(codigo, nombre, categoria, stock):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO productos (codigo, nombre, categoria, stock) VALUES (?, ?, ?, ?)",
                       (codigo, nombre, categoria, stock))
        registrar_movimiento_db("Alta", f"Producto: {nombre} ({codigo}), Stock: {stock}")
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def eliminar_producto_db(codigo):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
        if cursor.rowcount > 0:
            registrar_movimiento_db("Baja", f"Producto eliminado: Código {codigo}")
            conn.commit()
            return True
        return False
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def actualizar_producto_db(codigo, nuevo_nombre, nueva_categoria, nuevo_stock):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE productos SET nombre = ?, categoria = ?, stock = ? WHERE codigo = ?",
                       (nuevo_nombre, nueva_categoria, nuevo_stock, codigo))
        if cursor.rowcount > 0:
            registrar_movimiento_db("Modificación", f"Producto: {nuevo_nombre} ({codigo}) actualizado. Nuevo stock: {nuevo_stock}")
            conn.commit()
            return True
        return False
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def obtener_productos_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nombre, categoria, stock FROM productos")
    productos = [{"codigo": row[0], "nombre": row[1], "categoria": row[2], "stock": row[3]} for row in cursor.fetchall()]
    conn.close()
    return productos

# --- Movimientos ---
def registrar_movimiento_db(tipo, detalle):
    conn = conectar_db()
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("INSERT INTO movimientos (fecha, tipo, detalle) VALUES (?, ?, ?)",
                       (fecha, tipo, detalle))
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def obtener_movimientos_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, tipo, detalle FROM movimientos ORDER BY fecha DESC LIMIT 10")
    movimientos = cursor.fetchall()
    conn.close()
    return movimientos

# --- Préstamos ---
def registrar_prestamo_db(codigo_producto, solicitante, cantidad, fecha_devolucion_esperada):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT stock FROM productos WHERE codigo = ?", (codigo_producto,))
        resultado_stock = cursor.fetchone()
        if not resultado_stock or resultado_stock[0] < cantidad:
            return False, "Stock insuficiente o producto no encontrado."
        fecha_prestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO prestamos (codigo_producto, solicitante, cantidad, fecha_prestamo, fecha_devolucion_esperada, estado) VALUES (?, ?, ?, ?, ?, ?)",
            (codigo_producto, solicitante, cantidad, fecha_prestamo, fecha_devolucion_esperada, 'Prestado')
        )
        cursor.execute("UPDATE productos SET stock = stock - ? WHERE codigo = ?", (cantidad, codigo_producto))
        registrar_movimiento_db("Préstamo", f"'{cantidad}' de '{codigo_producto}' prestado a '{solicitante}'. Devolución esperada: {fecha_devolucion_esperada}")
        conn.commit()
        return True, "Préstamo registrado exitosamente."
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Error en la base de datos: {e}"
    finally:
        conn.close()

def registrar_devolucion_db(prestamo_id):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT codigo_producto, cantidad FROM prestamos WHERE id = ? AND estado = 'Prestado'", (prestamo_id,))
        prestamo = cursor.fetchone()
        if not prestamo:
            return False, "Préstamo no encontrado o ya devuelto."
        codigo_producto, cantidad_devuelta = prestamo
        fecha_devolucion_real = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE prestamos SET estado = 'Devuelto', fecha_devolucion_real = ? WHERE id = ?",
                       (fecha_devolucion_real, prestamo_id))
        cursor.execute("UPDATE productos SET stock = stock + ? WHERE codigo = ?",
                       (cantidad_devuelta, codigo_producto))
        registrar_movimiento_db("Devolución", f"Préstamo ID {prestamo_id} devuelto. '{cantidad_devuelta}' de '{codigo_producto}' reingresado.")
        conn.commit()
        return True, "Devolución registrada exitosamente."
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Error en la base de datos: {e}"
    finally:
        conn.close()

def obtener_prestamos_db(estado=None):
    conn = conectar_db()
    cursor = conn.cursor()
    query = """
        SELECT
            p.id,
            prod.nombre AS nombre_producto,
            p.solicitante,
            p.cantidad,
            p.fecha_prestamo,
            p.fecha_devolucion_esperada,
            p.fecha_devolucion_real,
            p.estado
        FROM prestamos AS p
        JOIN productos AS prod ON p.codigo_producto = prod.codigo
    """
    params = []
    if estado:
        query += " WHERE p.estado = ?"
        params.append(estado)
    query += " ORDER BY p.fecha_prestamo DESC"
    cursor.execute(query, params)
    prestamos = [{
        "id": row[0],
        "nombre_producto": row[1],
        "solicitante": row[2],
        "cantidad": row[3],
        "fecha_prestamo": row[4],
        "fecha_devolucion_esperada": row[5],
        "fecha_devolucion_real": row[6],
        "estado": row[7]
    } for row in cursor.fetchall()]
    conn.close()
    return prestamos

# --- Usuarios ---
def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verificar_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def registrar_usuario_db(username, password, rol='usuario'):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        hashed_pw = hash_password(password)
        cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                       (username, hashed_pw, rol))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def verificar_credenciales_db(username, password):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE username = ?", (username,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        hashed_password = resultado[0]
        return verificar_password(password, hashed_password)
    return False