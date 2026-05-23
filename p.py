import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ==========================================
# FUNCIONES
# ==========================================

def validar_numeros(texto):
    return texto.isdigit() or texto == ""

def limpiar_campos():
    entrada_id.delete(0, tk.END)
    entrada_nombre.delete(0, tk.END)
    entrada_editorial.delete(0, tk.END)
    entrada_autor.delete(0, tk.END)
    entrada_copias.delete(0, tk.END)

    frame_pregunta.grid_remove()

def guardar_datos():

    id_libro = entrada_id.get()
    nombre = entrada_nombre.get()
    editorial = entrada_editorial.get()
    autor = entrada_autor.get()
    copias = entrada_copias.get()

    if id_libro == "" or nombre == "" or editorial == "" or autor == "" or copias == "":
        messagebox.showwarning("Campos vacíos", "Debe completar todos los campos")
        return

    tabla.insert(
        "",
        tk.END,
        values=(id_libro, nombre, editorial, autor, copias, fecha_actual)
    )

    messagebox.showinfo("Guardado", "Libro guardado correctamente")

    limpiar_campos()

def seleccionar_fila(event):

    global item_seleccionado

    seleccion = tabla.focus()

    if seleccion == "":
        return

    item_seleccionado = seleccion

    valores = tabla.item(seleccion, "values")

    limpiar_campos()

    entrada_id.insert(0, valores[0])
    entrada_nombre.insert(0, valores[1])
    entrada_editorial.insert(0, valores[2])
    entrada_autor.insert(0, valores[3])
    entrada_copias.insert(0, valores[4])

def editar_datos():

    try:
        tabla.item(
            item_seleccionado,
            values=(
                entrada_id.get(),
                entrada_nombre.get(),
                entrada_editorial.get(),
                entrada_autor.get(),
                entrada_copias.get(),
                fecha_actual
            )
        )

        messagebox.showinfo("Editar", "Registro actualizado correctamente")
        limpiar_campos()

    except:
        messagebox.showwarning("Editar", "Seleccione un registro")

def eliminar_datos():

    try:
        seleccion = tabla.focus()

        if seleccion == "":
            messagebox.showwarning("Eliminar", "Seleccione un registro")
            return

        respuesta = messagebox.askyesno("Eliminar", "¿Desea eliminar el registro?")

        if respuesta:
            tabla.delete(seleccion)
            messagebox.showinfo("Eliminar", "Registro eliminado correctamente")
            limpiar_campos()

    except:
        messagebox.showerror("Error", "No se pudo eliminar")

def nuevo_registro():
    limpiar_campos()
    frame_pregunta.grid(row=0, column=0, padx=20)

def mostrar_datos():
    cantidad = len(tabla.get_children())
    messagebox.showinfo("Datos", f"Total de libros registrados: {cantidad}")

def salir_app():
    respuesta = messagebox.askyesno(
        "Salir",
        "¿Estás seguro de que quieres salir?"
    )
    if respuesta:
        ventana.destroy()

# ==========================================
# VENTANA PRINCIPAL
# ==========================================

ventana = tk.Tk()
ventana.title("Biblioteca UDI")
ventana.geometry("1200x700")
ventana.config(bg="white")

item_seleccionado = ""

# ==========================================
# TITULO
# ==========================================

tk.Label(
    ventana,
    text="SISTEMA DE GESTIÓN DE BIBLIOTECA UDI",
    font=("Arial", 20, "bold"),
    bg="white"
).pack(pady=15)

# ==========================================
# FORMULARIO CON VALIDACIONES
# ==========================================

frame_formulario = tk.Frame(ventana, bg="white")
frame_formulario.pack()

fecha_actual = datetime.now().strftime("%d/%m/%Y")

def limitar(P, max_len):
    return len(P) <= max_len or P == ""

vcmd10 = ventana.register(lambda P: limitar(P, 10))
vcmd100 = ventana.register(lambda P: limitar(P, 100))
vcmd3num = ventana.register(lambda P: (P.isdigit() and len(P) <= 3) or P == "")

# FECHA
tk.Label(frame_formulario, text="FECHA DE INGRESO", bg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
tk.Label(frame_formulario, text=fecha_actual, bg="white", relief="solid", width=12).grid(row=0, column=1)

# ID LIBRO
tk.Label(frame_formulario, text="ID LIBRO (máx 10 caracteres)", bg="white", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w")
entrada_id = tk.Entry(frame_formulario, width=40, validate="key", validatecommand=(vcmd10, "%P"))
entrada_id.grid(row=1, column=1)

# NOMBRE
tk.Label(frame_formulario, text="NOMBRE DEL LIBRO (máx 100)", bg="white", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w")
entrada_nombre = tk.Entry(frame_formulario, width=40, validate="key", validatecommand=(vcmd100, "%P"))
entrada_nombre.grid(row=2, column=1)

# EDITORIAL
tk.Label(frame_formulario, text="EDITORIAL (máx 100)", bg="white", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w")
entrada_editorial = tk.Entry(frame_formulario, width=40, validate="key", validatecommand=(vcmd100, "%P"))
entrada_editorial.grid(row=3, column=1)

# AUTOR
tk.Label(frame_formulario, text="AUTOR (máx 100)", bg="white", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky="w")
entrada_autor = tk.Entry(frame_formulario, width=40, validate="key", validatecommand=(vcmd100, "%P"))
entrada_autor.grid(row=4, column=1)

# COPIAS
tk.Label(frame_formulario, text="NUMERO DE COPIAS (máx 3 números)", bg="white", font=("Arial", 12, "bold")).grid(row=5, column=0, sticky="w")
entrada_copias = tk.Entry(frame_formulario, width=10, validate="key", validatecommand=(vcmd3num, "%P"))
entrada_copias.grid(row=5, column=1, sticky="w")

# ==========================================
# FRAME INFERIOR
# ==========================================

frame_inferior = tk.Frame(ventana, bg="white")
frame_inferior.pack(pady=30)

frame_pregunta = tk.Frame(frame_inferior, bg="white", bd=2, relief="solid")
frame_pregunta.grid(row=0, column=0, padx=20)
frame_pregunta.grid_remove()

tk.Label(frame_pregunta, text="Desea guardar\ncambios ?", bg="white", font=("Arial", 12, "bold")).pack(padx=10, pady=10)

frame_si_no = tk.Frame(frame_pregunta, bg="white")
frame_si_no.pack(pady=10)

tk.Button(frame_si_no, text="Si", width=8, command=guardar_datos).grid(row=0, column=0, padx=15)
tk.Button(frame_si_no, text="No", width=8, command=limpiar_campos).grid(row=0, column=1, padx=15)

# ==========================================
# TABLA
# ==========================================

frame_tabla = tk.Frame(frame_inferior, bg="white")
frame_tabla.grid(row=0, column=1)

frame_botones = tk.Frame(frame_tabla, bg="white")
frame_botones.pack(pady=5)

tk.Button(frame_botones, text="Nuevo", width=12, command=nuevo_registro).grid(row=0, column=0, padx=8)
tk.Button(frame_botones, text="Editar", width=12, command=editar_datos).grid(row=0, column=1, padx=8)
tk.Button(frame_botones, text="Guardar", width=12, command=guardar_datos).grid(row=0, column=2, padx=8)
tk.Button(frame_botones, text="Eliminar", width=12, command=eliminar_datos).grid(row=0, column=3, padx=8)

tabla = ttk.Treeview(frame_tabla, columns=("id","nombre","editorial","autor","copias","fecha"), show="headings", height=8)

for col, txt in zip(("id","nombre","editorial","autor","copias","fecha"),
                    ("Id Libro","Nombre Libro","Editorial","Autor","Num. copias","Fecha")):
    tabla.heading(col, text=txt)

tabla.pack()

tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

# ==========================================
# BOTONES INFERIORES
# ==========================================

frame_botones_inferiores = tk.Frame(ventana, bg="white")
frame_botones_inferiores.pack(pady=20)

tk.Button(frame_botones_inferiores, text="Cancelar", width=15, command=limpiar_campos).grid(row=0, column=0, padx=20)
tk.Button(frame_botones_inferiores, text="Mostrar datos", width=15, command=mostrar_datos).grid(row=0, column=1, padx=20)
tk.Button(frame_botones_inferiores, text="Salir", width=15, bg="red", fg="white", command=salir_app).grid(row=0, column=2, padx=20)

# ==========================================
# DATOS DE PRUEBA
# ==========================================

tabla.insert("", tk.END, values=("LB001","Cien años de soledad","Editorial Norma","Gabriel García Márquez","5","10/06/2025"))
tabla.insert("", tk.END, values=("LB002","Don Quijote de la Mancha","Alfaguara","Miguel de Cervantes","3","11/06/2025"))
tabla.insert("", tk.END, values=("LB003","La Odisea","Planeta","Homero","7","12/06/2025"))
tabla.insert("", tk.END, values=("LB004","El Principito","Santillana","Antoine de Saint-Exupéry","4","13/06/2025"))
tabla.insert("", tk.END, values=("LB005","Harry Potter","Salamandra","J.K. Rowling","10","14/06/2025"))

# ==========================================
# EJECUTAR
# ==========================================

ventana.mainloop()