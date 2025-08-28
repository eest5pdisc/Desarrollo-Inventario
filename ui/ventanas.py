import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import funciones as db
from ui.estilos import configurar_estilos

class MainApplication(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        configurar_estilos()
        self.title("Sistema de Inventario Informático Escolar")
        self.geometry("1100x750")
        self.state('normal')
        self.withdraw()

        self.secciones = {}
        self.create_main_widgets()
        self.deiconify()
        self.actualizar_tablas_inventario()
        # Creación de widgets de la ventana principal
    def create_main_widgets(self):
        # PANEL PRINCIPAL
        panel = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        panel.pack(fill="both", expand=True)

        # PANEL IZQUIERDO (Botonera)
        listado = tk.Frame(panel, bg="#34495E", width=180)
        listado.pack_propagate(False)
        panel.add(listado)

        tk.Label(listado, text="Menú Principal", bg="#34495E", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

        botones = ["Inicio", "Alta", "Bajas", "Modificaciones", "Préstamos", "Proyectos", "Mantenimiento"]

        # PANEL DERECHO (Contenedor dinámico)
        contenedor = tk.Frame(panel, bg="lightgray")
        contenedor.pack_propagate(False)
        panel.add(contenedor)

        # --- FUNCIONES GENERALES DE LA APLICACIÓN PRINCIPAL ---
        def mostrar_seccion(nombre):
            """Oculta todas las secciones y muestra la seleccionada."""
            for frame in self.secciones.values():
                frame.pack_forget()
            frame = self.secciones.get(nombre)
            if frame:
                frame.pack(fill="both", expand=True)
                # Si la sección es Préstamos, asegurarnos de cargar los productos y préstamos
                if nombre == "Préstamos":
                    cargar_productos_en_prestamo_combo()
                    actualizar_tabla_prestamos() # Actualiza los préstamos activos
                    actualizar_historial_prestamos() # Actualiza el historial completo
            
            # Opcional: Resaltar el botón activo en el menú
            for btn in listado.winfo_children():
                if isinstance(btn, ttk.Button):
                    if btn.cget("text") == nombre:
                        btn.state(['pressed'])
                    else:
                        btn.state(['!pressed'])

        # Esto se convierte en un método de la clase
        self.actualizar_tablas_inventario = lambda: self._actualizar_tablas_inventario(
            mov_tree, tabla_bajas, tabla_mod, resumen_frame,
            cargar_productos_en_prestamo_combo, actualizar_tabla_prestamos, actualizar_historial_prestamos
        )

        # --------------------------- SECCION: INICIO ---------------------------
        frame_inicio = tk.Frame(contenedor, bg="white")
        self.secciones["Inicio"] = frame_inicio

        ttk.Label(frame_inicio, text="Resumen del Inventario", font=("Arial", 16, "bold"), foreground="#2C3E50").pack(anchor="w", padx=20, pady=(20, 10))

        # Tarjetas resumen
        resumen_frame = tk.Frame(frame_inicio, bg="white")
        resumen_frame.pack(fill="x", padx=20, pady=10)

        def crear_tarjeta(master, color, cantidad, texto):
            frame = tk.Frame(master, bg=color, width=150, height=80, relief="flat", bd=0)
            frame.pack_propagate(False)
            frame.pack(side="left", padx=10, pady=5)
            tk.Label(frame, text=str(cantidad), font=("Arial", 18, "bold"), bg=color, fg="white").pack(pady=(5,2))
            tk.Label(frame, text=texto, font=("Arial", 11), bg=color, fg="white").pack()

        # Valores iniciales de ejemplo (se actualizarán con actualizar_tablas_inventario)
        crear_tarjeta(resumen_frame, "#1ABC9C", 0, "Recursos Totales")
        crear_tarjeta(resumen_frame, "#3498DB", 0, "Préstamos Activos")
        crear_tarjeta(resumen_frame, "#E67E22", 0, "Proyectos en Curso")
        crear_tarjeta(resumen_frame, "#9B59B6", 0, "Pendientes Devolución")

        # Últimos movimientos
        movimientos_frame = tk.Frame(frame_inicio, bg="white")
        movimientos_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ttk.Label(movimientos_frame, text="Últimos Movimientos", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))

        mov_tree = ttk.Treeview(movimientos_frame, columns=("Fecha", "Tipo", "Detalle"), show="headings", height=8)
        mov_tree.heading("Fecha", text="Fecha")
        mov_tree.heading("Tipo", text="Tipo")
        mov_tree.heading("Detalle", text="Detalle")
        mov_tree.column("Fecha", width=120, anchor="center")
        mov_tree.column("Tipo", width=150, anchor="center")
        mov_tree.column("Detalle", width=500, stretch=True)
        mov_tree.pack(fill="both", expand=True)

        # Añadir Scrollbar al Treeview de movimientos
        mov_tree_scrollbar_y = ttk.Scrollbar(mov_tree, orient="vertical", command=mov_tree.yview)
        mov_tree.configure(yscrollcommand=mov_tree_scrollbar_y.set)
        mov_tree_scrollbar_y.pack(side="right", fill="y")


        # --------------------------- SECCION: ALTA ---------------------------
        frame_alta = tk.Frame(contenedor, bg="white")
        self.secciones["Alta"] = frame_alta

        ttk.Label(frame_alta, text="Registrar Nuevo Recurso", font=("Arial", 16, "bold"), foreground="#2C3E50").pack(anchor="w", padx=40, pady=(20, 10))

        form_alta = tk.Frame(frame_alta, bg="white")
        form_alta.pack(padx=40, pady=10, fill="x")

        form_alta.grid_columnconfigure(1, weight=1)

        ttk.Label(form_alta, text="Código:").grid(row=0, column=0, sticky="e", pady=5, padx=10)
        entry_codigo = ttk.Entry(form_alta)
        entry_codigo.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(form_alta, text="Nombre:").grid(row=1, column=0, sticky="e", pady=5, padx=10)
        entry_nombre = ttk.Entry(form_alta)
        entry_nombre.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(form_alta, text="Categoría:").grid(row=2, column=0, sticky="e", pady=5, padx=10)
        combo_categoria = ttk.Combobox(form_alta, values=["Computadoras", "Tabletas", "Proyectores", "Impresoras", "Redes", "Periféricos", "Otros"], state="readonly")
        combo_categoria.set("Selecciona una categoría")
        combo_categoria.grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(form_alta, text="Stock:").grid(row=3, column=0, sticky="e", pady=5, padx=10)
        spin_stock = tk.Spinbox(form_alta, from_=0, to=1000, font=("Arial", 9), width=10)
        spin_stock.grid(row=3, column=1, sticky="w", pady=5)

        def guardar_producto():
            codigo = entry_codigo.get().strip()
            nombre = entry_nombre.get().strip()
            categoria = combo_categoria.get()
            stock = spin_stock.get()

            if not codigo or not nombre or categoria == "Selecciona una categoría":
                messagebox.showwarning("Advertencia", "Completá todos los campos para dar de alta un producto.")
                return

            try:
                stock = int(stock)
                if stock < 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Advertencia", "El stock debe ser un número entero no negativo.")
                return

            if db.agregar_producto_db(codigo, nombre, categoria, stock):
                messagebox.showinfo("Éxito", "Producto guardado correctamente.")
                entry_codigo.delete(0, tk.END)
                entry_nombre.delete(0, tk.END)
                combo_categoria.set("Selecciona una categoría")
                spin_stock.delete(0, tk.END)
                spin_stock.insert(0, 0)
                self.actualizar_tablas_inventario()
            else:
                messagebox.showerror("Error", f"No se pudo guardar el producto. El código '{codigo}' probablemente ya existe o hubo otro error en la base de datos.")

        ttk.Button(form_alta, text="Guardar Producto", command=guardar_producto, style="Primary.TButton").grid(row=4, column=0, columnspan=2, pady=20)


        # --------------------------- SECCION: BAJAS ---------------------------
        frame_bajas = tk.Frame(contenedor, bg="white")
        self.secciones["Bajas"] = frame_bajas

        ttk.Label(frame_bajas, text="Eliminar Recurso", font=("Arial", 16, "bold"), foreground="#2C3E50").pack(anchor="w", padx=20, pady=(20, 10))

        bajas_table_frame = tk.Frame(frame_bajas, bg="white")
        bajas_table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        tabla_bajas = ttk.Treeview(bajas_table_frame, columns=("Codigo", "Nombre", "Categoria", "Stock"), show="headings", height=8)
        tabla_bajas.heading("Codigo", text="Código")
        tabla_bajas.heading("Nombre", text="Nombre")
        tabla_bajas.heading("Categoria", text="Categoría")
        tabla_bajas.heading("Stock", text="Stock")

        for col in ("Codigo", "Nombre", "Categoria", "Stock"):
            tabla_bajas.column(col, anchor="center")

        tabla_bajas.column("Codigo", width=100)
        tabla_bajas.column("Nombre", width=200, stretch=True)
        tabla_bajas.column("Categoria", width=150)
        tabla_bajas.column("Stock", width=80)

        tabla_bajas.pack(side="left", fill="both", expand=True)

        bajas_scrollbar_y = ttk.Scrollbar(bajas_table_frame, orient="vertical", command=tabla_bajas.yview)
        tabla_bajas.configure(yscrollcommand=bajas_scrollbar_y.set)
        bajas_scrollbar_y.pack(side="right", fill="y")


        def eliminar_producto_ui():
            seleccion = tabla_bajas.selection()
            if seleccion:
                item = tabla_bajas.item(seleccion[0])
                codigo_a_eliminar = item['values'][0]

                if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el producto con código: {codigo_a_eliminar}?"):
                    if db.eliminar_producto_db(codigo_a_eliminar):
                        messagebox.showinfo("Éxito", f"Producto con código {codigo_a_eliminar} eliminado correctamente.")
                        self.actualizar_tablas_inventario()
                    else:
                        messagebox.showerror("Error", f"No se pudo eliminar el producto con código {codigo_a_eliminar}. Puede que no exista o hubo un error en la base de datos.")
            else:
                messagebox.showwarning("Advertencia", "Seleccioná un producto de la tabla para eliminarlo.")

        ttk.Button(frame_bajas, text="Eliminar seleccionado", command=eliminar_producto_ui,
                   style="Danger.TButton").pack(pady=20)


        # --------------------------- SECCION: MODIFICACIONES ---------------------------
        frame_modificaciones = tk.Frame(contenedor, bg="white")
        self.secciones["Modificaciones"] = frame_modificaciones

        ttk.Label(frame_modificaciones, text="Modificar Recurso Existente", font=("Arial", 16, "bold"), foreground="#2C3E50").pack(anchor="w", padx=20, pady=(20, 10))

        mod_table_frame = tk.Frame(frame_modificaciones, bg="white")
        mod_table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        tabla_mod = ttk.Treeview(mod_table_frame, columns=("Codigo", "Nombre", "Categoria", "Stock"), show="headings", height=6)
        tabla_mod.heading("Codigo", text="Código")
        tabla_mod.heading("Nombre", text="Nombre")
        tabla_mod.heading("Categoria", text="Categoría")
        tabla_mod.heading("Stock", text="Stock")

        for col in ("Codigo", "Nombre", "Categoria", "Stock"):
            tabla_mod.column(col, anchor="center")

        tabla_mod.column("Codigo", width=100)
        tabla_mod.column("Nombre", width=200, stretch=True)
        tabla_mod.column("Categoria", width=150)
        tabla_mod.column("Stock", width=80)

        tabla_mod.pack(side="left", fill="both", expand=True)

        mod_scrollbar_y = ttk.Scrollbar(mod_table_frame, orient="vertical", command=tabla_mod.yview)
        tabla_mod.configure(yscrollcommand=mod_scrollbar_y.set)
        mod_scrollbar_y.pack(side="right", fill="y")

        # Formulario de modificación
        form_mod = tk.Frame(frame_modificaciones, bg="white")
        form_mod.pack(padx=20, pady=10, fill="x")
        form_mod.grid_columnconfigure(1, weight=1)

        ttk.Label(form_mod, text="Nombre:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        entry_nombre_mod = ttk.Entry(form_mod)
        entry_nombre_mod.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(form_mod, text="Categoría:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        combo_categoria_mod = ttk.Combobox(form_mod, values=["Computadoras", "Tabletas", "Proyectores", "Impresoras", "Redes", "Periféricos", "Otros"], state="readonly")
        combo_categoria_mod.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(form_mod, text="Stock:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        spin_stock_mod = tk.Spinbox(form_mod, from_=0, to=1000, font=("Arial", 9), width=10)
        spin_stock_mod.grid(row=2, column=1, sticky="w", pady=5)


        def cargar_producto_mod(event):
            """Carga los datos del producto seleccionado en el formulario de modificación."""
            seleccion = tabla_mod.selection()
            if seleccion:
                item = tabla_mod.item(seleccion[0])
                prod_values = item['values']

                entry_nombre_mod.delete(0, tk.END)
                entry_nombre_mod.insert(0, prod_values[1])

                combo_categoria_mod.set(prod_values[2])

                spin_stock_mod.delete(0, tk.END)
                spin_stock_mod.insert(0, prod_values[3])
            else:
                entry_nombre_mod.delete(0, tk.END)
                combo_categoria_mod.set("")
                spin_stock_mod.delete(0, tk.END)
                spin_stock_mod.insert(0, 0)

        tabla_mod.bind("<<TreeviewSelect>>", cargar_producto_mod)

        def actualizar_producto_ui():
            seleccion = tabla_mod.selection()
            if seleccion:
                item = tabla_mod.item(seleccion[0])
                codigo_a_actualizar = item['values'][0]

                nuevo_nombre = entry_nombre_mod.get().strip()
                nueva_categoria = combo_categoria_mod.get()
                nuevo_stock = spin_stock_mod.get()

                if not nuevo_nombre or not nueva_categoria or nueva_categoria == "Selecciona una categoría":
                    messagebox.showwarning("Advertencia", "Completá todos los campos para la actualización.")
                    return
                
                try:
                    nuevo_stock = int(nuevo_stock)
                    if nuevo_stock < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showwarning("Advertencia", "El stock debe ser un número entero no negativo.")
                    return

                if db.actualizar_producto_db(codigo_a_actualizar, nuevo_nombre, nueva_categoria, nuevo_stock):
                    messagebox.showinfo("Éxito", f"Producto con código {codigo_a_actualizar} actualizado correctamente.")
                    self.actualizar_tablas_inventario()
                    entry_nombre_mod.delete(0, tk.END)
                    combo_categoria_mod.set("Selecciona una categoría")
                    spin_stock_mod.delete(0, tk.END)
                    spin_stock_mod.insert(0, 0)
                else:
                    messagebox.showerror("Error", f"No se pudo actualizar el producto con código {codigo_a_actualizar}. Puede que no exista o hubo un error en la base de datos.")
            else:
                messagebox.showwarning("Atención", "Seleccioná un producto primero de la tabla para modificarlo.")

        btn_actualizar = ttk.Button(frame_modificaciones, text="Actualizar Producto", command=actualizar_producto_ui,
                                    style="Primary.TButton")
        btn_actualizar.pack(pady=10)


        # --------------------------- SECCION: PRÉSTAMOS ---------------------------
        frame_prestamos = tk.Frame(contenedor, bg="white")
        self.secciones["Préstamos"] = frame_prestamos

        ttk.Label(frame_prestamos, text="Registrar Préstamo", font=("Arial", 16, "bold"), foreground="#2C3E50").pack(anchor="w", padx=20, pady=(20, 10))

        prestamo_frame_form = tk.Frame(frame_prestamos, bg="white", padx=30, pady=20, relief="groove", bd=2)
        prestamo_frame_form.pack(pady=10, padx=20, fill="x")

        prestamo_frame_form.grid_columnconfigure(1, weight=1)

        ttk.Label(prestamo_frame_form, text="Solicitante:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
        entry_solicitante = ttk.Entry(prestamo_frame_form, font=("Arial", 10))
        entry_solicitante.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(prestamo_frame_form, text="Producto:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5, padx=5)
        combo_elemento_prestamo = ttk.Combobox(prestamo_frame_form, state="readonly", font=("Arial", 10))
        combo_elemento_prestamo.grid(row=1, column=1, pady=5, sticky="ew")

        producto_seleccionado_codigo = ""
        producto_seleccionado_stock = 0

        def cargar_productos_en_prestamo_combo():
            """Carga los productos disponibles en el Combobox de la sección Préstamos."""
            nonlocal producto_seleccionado_codigo, producto_seleccionado_stock # Para modificar las variables de este ámbito
            productos = db.obtener_productos_db()
            nombres_codigos = [f"{p['nombre']} ({p['codigo']})" for p in productos if p['stock'] > 0]
            combo_elemento_prestamo['values'] = nombres_codigos
            combo_elemento_prestamo.set("Selecciona un producto")
            spin_cantidad_prestamo.delete(0, tk.END)
            spin_cantidad_prestamo.insert(0, 1)
            producto_seleccionado_codigo = "" # Resetear al cargar
            producto_seleccionado_stock = 0

        def on_producto_prestamo_select(event):
            """Actualiza el spinbox de cantidad según el stock del producto seleccionado."""
            nonlocal producto_seleccionado_codigo, producto_seleccionado_stock # Para modificar las variables de este ámbito
            seleccion_texto = combo_elemento_prestamo.get()
            if seleccion_texto:
                try:
                    codigo_inicio = seleccion_texto.rfind('(') + 1
                    codigo_fin = seleccion_texto.rfind(')')
                    codigo = seleccion_texto[codigo_inicio:codigo_fin]
                    
                    productos = db.obtener_productos_db()
                    for p in productos:
                        if p['codigo'] == codigo:
                            producto_seleccionado_codigo = p['codigo']
                            producto_seleccionado_stock = p['stock']
                            spin_cantidad_prestamo.config(to=producto_seleccionado_stock)
                            spin_cantidad_prestamo.delete(0, tk.END)
                            spin_cantidad_prestamo.insert(0, 1)
                            break
                except Exception:
                    producto_seleccionado_codigo = ""
                    producto_seleccionado_stock = 0
                    spin_cantidad_prestamo.config(to=1)
                    spin_cantidad_prestamo.delete(0, tk.END)
                    spin_cantidad_prestamo.insert(0, 1)
                    
        combo_elemento_prestamo.bind("<<ComboboxSelected>>", on_producto_prestamo_select)

        ttk.Label(prestamo_frame_form, text="Cantidad:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", pady=5, padx=5)
        spin_cantidad_prestamo = tk.Spinbox(prestamo_frame_form, from_=1, to=1, font=("Arial", 10), width=10)
        spin_cantidad_prestamo.grid(row=2, column=1, pady=5, sticky="w")

        ttk.Label(prestamo_frame_form, text="Fecha de devolución (YYYY-MM-DD):", font=("Arial", 10)).grid(row=3, column=0, sticky="e", pady=5, padx=5)
        entry_fecha_devolucion = ttk.Entry(prestamo_frame_form, font=("Arial", 10))
        entry_fecha_devolucion.insert(0, (datetime.now().date()).strftime("%Y-%m-%d")) # Fecha actual del día, sin hora
        entry_fecha_devolucion.grid(row=3, column=1, pady=5, sticky="ew")

        def registrar_prestamo_ui():
            solicitante = entry_solicitante.get().strip()
            codigo_producto = producto_seleccionado_codigo 
            cantidad_str = spin_cantidad_prestamo.get()
            fecha_devolucion_esperada = entry_fecha_devolucion.get().strip()

            if not solicitante or not codigo_producto or not cantidad_str or not fecha_devolucion_esperada:
                messagebox.showwarning("Advertencia", "Por favor, completa todos los campos del préstamo.")
                return

            try:
                cantidad = int(cantidad_str)
                if cantidad <= 0:
                    messagebox.showwarning("Advertencia", "La cantidad debe ser un número positivo.")
                    return
                if cantidad > producto_seleccionado_stock:
                    messagebox.showwarning("Advertencia", f"No hay suficiente stock disponible. Stock actual: {producto_seleccionado_stock}.")
                    return
            except ValueError:
                messagebox.showwarning("Advertencia", "La cantidad debe ser un número entero válido.")
                return
            
            try: # Validar que la fecha de devolución esperada no sea anterior a la actual
                fecha_devolucion_dt = datetime.strptime(fecha_devolucion_esperada, "%Y-%m-%d").date()
                if fecha_devolucion_dt < datetime.now().date():
                    messagebox.showwarning("Advertencia", "La fecha de devolución esperada no puede ser anterior a la fecha actual.")
                    return
            except ValueError:
                messagebox.showwarning("Advertencia", "El formato de fecha de devolución debe ser YYYY-MM-DD.")
                return

            exito, mensaje = db.registrar_prestamo_db(codigo_producto, solicitante, cantidad, fecha_devolucion_esperada)

            if exito:
                messagebox.showinfo("Éxito", "Préstamo registrado correctamente.")
                entry_solicitante.delete(0, tk.END)
                combo_elemento_prestamo.set("Selecciona un producto")
                spin_cantidad_prestamo.delete(0, tk.END)
                spin_cantidad_prestamo.insert(0, 1)
                entry_fecha_devolucion.delete(0, tk.END)
                entry_fecha_devolucion.insert(0, (datetime.now().date()).strftime("%Y-%m-%d"))

                self.actualizar_tablas_inventario()
                cargar_productos_en_prestamo_combo()
            else:
                messagebox.showerror("Error", f"No se pudo registrar el préstamo: {mensaje}")

        ttk.Button(prestamo_frame_form, text="Registrar Préstamo", command=registrar_prestamo_ui,
                   style="Primary.TButton").grid(row=4, column=0, columnspan=2, pady=20)


        # TABLA DE PRÉSTAMOS ACTIVOS
        ttk.Label(frame_prestamos, text="Préstamos Activos", font=("Arial", 12, "bold"), foreground="#2C3E50").pack(anchor="w", padx=20, pady=(10, 5))

        prestamos_table_frame = tk.Frame(frame_prestamos, bg="white")
        prestamos_table_frame.pack(padx=20, pady=5, fill="both", expand=True)

        tabla_prestamos = ttk.Treeview(prestamos_table_frame,
                                       columns=("ID", "Producto", "Solicitante", "Cantidad", "F. Préstamo", "F. Devolución Esperada", "Estado"),
                                       show="headings", height=8)

        tabla_prestamos.heading("ID", text="ID")
        tabla_prestamos.heading("Producto", text="Producto")
        tabla_prestamos.heading("Solicitante", text="Solicitante")
        tabla_prestamos.heading("Cantidad", text="Cantidad")
        tabla_prestamos.heading("F. Préstamo", text="F. Préstamo")
        tabla_prestamos.heading("F. Devolución Esperada", text="F. Devolución Esperada")
        tabla_prestamos.heading("Estado", text="Estado")

        tabla_prestamos.column("ID", width=40, anchor="center")
        tabla_prestamos.column("Producto", width=150, stretch=True)
        tabla_prestamos.column("Solicitante", width=120)
        tabla_prestamos.column("Cantidad", width=70, anchor="center")
        tabla_prestamos.column("F. Préstamo", width=120, anchor="center")
        tabla_prestamos.column("F. Devolución Esperada", width=120, anchor="center")
        tabla_prestamos.column("Estado", width=80, anchor="center")

        tabla_prestamos.pack(side="left", fill="both", expand=True)

        prestamos_scrollbar_y = ttk.Scrollbar(prestamos_table_frame, orient="vertical", command=tabla_prestamos.yview)
        tabla_prestamos.configure(yscrollcommand=prestamos_scrollbar_y.set)
        prestamos_scrollbar_y.pack(side="right", fill="y")

        def actualizar_tabla_prestamos():
            """Carga los préstamos activos en la tabla de préstamos."""
            tabla_prestamos.delete(*tabla_prestamos.get_children())
            prestamos = db.obtener_prestamos_db(estado="Prestado")
            
            hoy = datetime.now().date()

            for p in prestamos:
                tags = ()
                if p['estado'] == 'Prestado':
                    try:
                        fecha_esperada_dt = datetime.strptime(p['fecha_devolucion_esperada'], "%Y-%m-%d").date()
                        if fecha_esperada_dt < hoy:
                            tags = ('tag_vencido',)
                    except (ValueError, TypeError): # Manejar errores si la fecha no es válida
                        pass
                
                tabla_prestamos.insert("", "end", values=(
                    p['id'], p['nombre_producto'], p['solicitante'], p['cantidad'],
                    p['fecha_prestamo'], p['fecha_devolucion_esperada'], p['estado']
                ), tags=tags)


        def registrar_devolucion_ui():
            seleccion = tabla_prestamos.selection()
            if seleccion:
                item = tabla_prestamos.item(seleccion[0])
                prestamo_id = item['values'][0]
                producto_nombre = item['values'][1]
                solicitante = item['values'][2]

                if messagebox.askyesno("Confirmar Devolución",
                                       f"¿Confirmas la devolución de '{producto_nombre}' por '{solicitante}' (ID: {prestamo_id})?"):
                    exito, mensaje = db.registrar_devolucion_db(prestamo_id)
                    if exito:
                        messagebox.showinfo("Éxito", "Devolución registrada correctamente.")
                        self.actualizar_tablas_inventario()
                        actualizar_tabla_prestamos() # Refrescar la tabla de préstamos activos
                        actualizar_historial_prestamos() # Refrescar el historial también
                    else:
                        messagebox.showerror("Error", f"No se pudo registrar la devolución: {mensaje}")
            else:
                messagebox.showwarning("Advertencia", "Selecciona un préstamo de la tabla para registrar su devolución.")

        ttk.Button(frame_prestamos, text="Registrar Devolución", command=registrar_devolucion_ui,
                   style="Success.TButton").pack(pady=10)


        # --- HISTORIAL COMPLETO DE PRÉSTAMOS ---
        ttk.Label(frame_prestamos, text="Historial Completo de Préstamos", font=("Arial", 12, "bold"), foreground="#2C3E50").pack(anchor="w", padx=20, pady=(10, 5))

        historial_prestamos_table_frame = tk.Frame(frame_prestamos, bg="white")
        historial_prestamos_table_frame.pack(padx=20, pady=5, fill="both", expand=True)

        tabla_historial_prestamos = ttk.Treeview(historial_prestamos_table_frame,
                                        columns=("ID", "Producto", "Solicitante", "Cantidad", "F. Préstamo", "F. Devolución Esperada", "F. Devolución Real", "Estado"),
                                        show="headings", height=8)

        tabla_historial_prestamos.heading("ID", text="ID")
        tabla_historial_prestamos.heading("Producto", text="Producto")
        tabla_historial_prestamos.heading("Solicitante", text="Solicitante")
        tabla_historial_prestamos.heading("Cantidad", text="Cantidad")
        tabla_historial_prestamos.heading("F. Préstamo", text="F. Préstamo")
        tabla_historial_prestamos.heading("F. Devolución Esperada", text="F. Dev. Esperada")
        tabla_historial_prestamos.heading("F. Devolución Real", text="F. Dev. Real")
        tabla_historial_prestamos.heading("Estado", text="Estado")

        tabla_historial_prestamos.column("ID", width=40, anchor="center")
        tabla_historial_prestamos.column("Producto", width=120, stretch=True)
        tabla_historial_prestamos.column("Solicitante", width=100)
        tabla_historial_prestamos.column("Cantidad", width=60, anchor="center")
        tabla_historial_prestamos.column("F. Préstamo", width=110, anchor="center")
        tabla_historial_prestamos.column("F. Devolución Esperada", width=110, anchor="center")
        tabla_historial_prestamos.column("F. Devolución Real", width=110, anchor="center")
        tabla_historial_prestamos.column("Estado", width=80, anchor="center")

        tabla_historial_prestamos.pack(side="left", fill="both", expand=True)

        historial_prestamos_scrollbar_y = ttk.Scrollbar(historial_prestamos_table_frame, orient="vertical", command=tabla_historial_prestamos.yview)
        tabla_historial_prestamos.configure(yscrollcommand=historial_prestamos_scrollbar_y.set)
        historial_prestamos_scrollbar_y.pack(side="right", fill="y")

        def actualizar_historial_prestamos():
            """Carga *todos* los préstamos en la tabla de historial y resalta vencidos."""
            tabla_historial_prestamos.delete(*tabla_historial_prestamos.get_children())
            all_prestamos = db.obtener_prestamos_db(estado=None)
            
            hoy = datetime.now().date()

            for p in all_prestamos:
                tags = ()
                try:
                    fecha_prestamo_str = p['fecha_prestamo'].split(" ")[0]
                    fecha_prestamo_dt = datetime.strptime(fecha_prestamo_str, "%Y-%m-%d").date()
                except (ValueError, AttributeError):
                    fecha_prestamo_str = p['fecha_prestamo'] # Usar original si falla
                    fecha_prestamo_dt = None

                try:
                    fecha_esperada_dt = datetime.strptime(p['fecha_devolucion_esperada'], "%Y-%m-%d").date()
                except (ValueError, AttributeError):
                    fecha_esperada_dt = None

                if p['estado'] == 'Prestado' and fecha_esperada_dt and fecha_esperada_dt < hoy:
                    tags = ('tag_vencido',)
                elif p['estado'] == 'Devuelto':
                    tags = ('tag_devuelto',)

                tabla_historial_prestamos.insert("", "end", values=(
                    p['id'], p['nombre_producto'], p['solicitante'], p['cantidad'],
                    fecha_prestamo_str,
                    p['fecha_devolucion_esperada'],
                    p['fecha_devolucion_real'].split(" ")[0] if p['fecha_devolucion_real'] else "N/A",
                    p['estado']
                ), tags=tags)

        # --------------------------- SECCION: PROYECTOS ---------------------------
        frame_proyectos = tk.Frame(contenedor, bg="white")
        self.secciones["Proyectos"] = frame_proyectos

        ttk.Label(frame_proyectos, text="Cargar Proyecto", font=("Arial", 16, "bold"), foreground="#2C3E50").pack(anchor="w", padx=20, pady=(20, 10))

        proyectos_frame = tk.Frame(frame_proyectos, bg="white", padx=30, pady=20, relief="groove", bd=2)
        proyectos_frame.pack(pady=10, padx=20, fill="x")

        proyectos_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(proyectos_frame, text="Título del proyecto:").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        entry_Titulo_Proyecto = ttk.Entry(proyectos_frame)
        entry_Titulo_Proyecto.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(proyectos_frame, text="Responsable:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        combo_responsable = ttk.Combobox(proyectos_frame, values=["Carolina Mtp", "Sara Neiret", "Guido Gandolfo"], state="readonly")
        combo_responsable.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(proyectos_frame, text="Fecha de inicio:").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        entry_fecha_inicio = ttk.Entry(proyectos_frame)
        entry_fecha_inicio.insert(0, "YYYY-MM-DD")
        entry_fecha_inicio.grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(proyectos_frame, text="Objetivo:").grid(row=3, column=0, sticky="ne", pady=5, padx=5)
        texto_objetivo = tk.Text(proyectos_frame, height=5, width=40, font=("Arial", 9))
        texto_objetivo.grid(row=3, column=1, sticky="ew", pady=5)

        ttk.Button(proyectos_frame, text="Guardar Proyecto",
                   #command=tu_funcion_guardar_proyecto, # <-- Descomentar y asignar función cuando se implemente
                   style="Primary.TButton").grid(row=4, column=0, columnspan=2, pady=20)


# --------------------------- SECCION: MANTENIMIENTO ---------------------------
        frame_mantenimiento = tk.Frame(contenedor, bg="white")
        self.secciones["Mantenimiento"] = frame_mantenimiento
        contenedor.add(frame_mantenimiento, text="Mantenimiento")

# Título
        ttk.Label(frame_mantenimiento, text="Gestión de Mantenimiento",
          font=("Arial", 18, "bold"), foreground="#2C3E50").pack(anchor="center", pady=15)

# ---------------- FORMULARIO ----------------
        form_frame = tk.Frame(frame_mantenimiento, bg="white", padx=20, pady=15, relief="groove", bd=2)
        form_frame.pack(pady=10, padx=20, fill="x")

# Equipo
        ttk.Label(form_frame, text="Equipo:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entry_equipo = ttk.Entry(form_frame)
        entry_equipo.grid(row=0, column=1, sticky="ew", pady=5)

# Responsables (MULTIPLE selección con Listbox)
        ttk.Label(form_frame, text="Responsables:").grid(row=1, column=0, sticky="ne", padx=5, pady=5)
        lista_responsables = tk.Listbox(form_frame, selectmode="multiple", height=4, exportselection=False)
        for resp in ["Carolina Mtp", "Sara Neiret", "Guido Gandolfo", "Otro técnico"]:
          lista_responsables.insert(tk.END, resp)
          lista_responsables.grid(row=1, column=1, sticky="ew", pady=5)
     
# Fecha (formato Argentino DD/MM/YYYY)
        ttk.Label(form_frame, text="Fecha:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        entry_fecha = ttk.Entry(form_frame)
        entry_fecha.insert(0, "DD/MM/YYYY")
        entry_fecha.grid(row=2, column=1, sticky="ew", pady=5)

# Tipo de mantenimiento
        ttk.Label(form_frame, text="Tipo:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        combo_tipo = ttk.Combobox(form_frame, 
                          values=["Preventivo", "Correctivo", "Evolutivo"], 
                          state="readonly")
        combo_tipo.grid(row=3, column=1, sticky="ew", pady=5)

# Descripción
        ttk.Label(form_frame, text="Descripción:").grid(row=4, column=0, sticky="ne", padx=5, pady=5)
        texto_desc = tk.Text(form_frame, height=4, width=40, font=("Arial", 9))
        texto_desc.grid(row=4, column=1, sticky="ew", pady=5)

# Botón guardar
        ttk.Button(form_frame, text="Guardar Mantenimiento",
           style="Primary.TButton"
           # command=self.guardar_mantenimiento
           ).grid(row=5, column=0, columnspan=2, pady=15)

        form_frame.grid_columnconfigure(1, weight=1)

# ---------------- HISTORIAL (Treeview con Scrollbar) ----------------
        tabla_frame = tk.Frame(frame_mantenimiento, bg="white")
        tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("Equipo", "Responsables", "Fecha", "Tipo", "Descripción")
        tabla_mant = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=8)

        for col in cols:
          tabla_mant.heading(col, text=col)
          tabla_mant.column(col, width=150, anchor="center")

# Scrollbar vertical
        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla_mant.yview)
        tabla_mant.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")

# Scrollbar horizontal
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal", command=tabla_mant.xview)
        tabla_mant.configure(xscroll=scroll_x.set)
        scroll_x.pack(side="bottom", fill="x")

        tabla_mant.pack(fill="both", expand=True)








        # --------------------------- BOTONERA FUNCIONAL ---------------------------
        for texto in botones:
            ttk.Button(listado, text=texto, style="Menu.TButton",
                       command=lambda t=texto: mostrar_seccion(t)).pack(pady=5, fill="x", padx=10)

        # Mostrar inicio por defecto al principio
            mostrar_seccion("Inicio")


    # Función actualizada para la clase
            def _actualizar_tablas_inventario(self, mov_tree, tabla_bajas, tabla_mod, resumen_frame,
                                      cargar_productos_en_prestamo_combo_func,
                                      actualizar_tabla_prestamos_func,
                                      actualizar_historial_prestamos_func):
             """
        Función para refrescar los datos de todas las tablas y resúmenes de la UI
        después de una operación de la base de datos.
        """
        # 1. Actualizar tabla de Movimientos (Inicio)
            mov_tree.delete(*mov_tree.get_children())
            movimientos_db = db.obtener_movimientos_db()
        for m in movimientos_db:
            mov_tree.insert("", "end", values=m)

        # 2. Actualizar tabla de Bajas
            tabla_bajas.delete(*tabla_bajas.get_children())
            productos_db = db.obtener_productos_db()
        for p in productos_db:
            tabla_bajas.insert("", "end", values=p)

        # 3. Actualizar tabla de Modificaciones
            tabla_mod.delete(*tabla_mod.get_children())
        for p in productos_db:
            tabla_mod.insert("", "end", values=p)

        # 4. Actualizar Tarjetas Resumen (Inicio)
            total_recursos = len(productos_db)
            prestamos_activos = db.obtener_prestamos_db(estado="Prestado")
            total_prestamos_activos = sum(p['cantidad'] for p in prestamos_activos)

        # Actualizar la tarjeta de Recursos Totales y Préstamos Activos
        # Se asume que las tarjetas mantienen el orden de creación
            tarjetas_labels = [c.winfo_children()[0] for c in resumen_frame.winfo_children() if isinstance(c, tk.Frame)]
            tarjetas_labels[0].config(text=str(total_recursos)) # Recursos Totales
            tarjetas_labels[1].config(text=str(total_prestamos_activos)) # Préstamos Activos
        # Las otras dos tarjetas (Proyectos en Curso, Pendientes Devolución) quedan en 0 por ahora

        # 5. Actualizar tablas de Préstamos
            cargar_productos_en_prestamo_combo_func()
            actualizar_tabla_prestamos_func()
            actualizar_historial_prestamos_func()

        # ...todo el código desde línea 85 a 767...