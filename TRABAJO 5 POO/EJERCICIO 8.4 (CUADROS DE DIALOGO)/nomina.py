import os
from enum import Enum
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


# ==========================================
# Enumerados
# ==========================================
class TipoCargo(Enum):
    DIRECTIVO = "Directivo"
    ESTRATEGICO = "Estratégico"
    OPERATIVO = "Operativo"


class TipoGenero(Enum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"


# ==========================================
# Clase: Empleado
# ==========================================
class Empleado:
    def __init__(self, nombre: str, apellidos: str, cargo: TipoCargo,
                 genero: TipoGenero, salario_dia: float, dias_trabajados: int,
                 otros_ingresos: float, pagos_salud: float, aporte_pensiones: float):
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__cargo = cargo
        self.__genero = genero
        self.__salario_dia = salario_dia
        self.__dias_trabajados = dias_trabajados
        self.__otros_ingresos = otros_ingresos
        self.__pagos_salud = pagos_salud
        self.__aporte_pensiones = aporte_pensiones

    def get_nombre(self) -> str:
        return self.__nombre

    def get_apellidos(self) -> str:
        return self.__apellidos

    def get_cargo(self) -> TipoCargo:
        return self.__cargo

    def get_genero(self) -> TipoGenero:
        return self.__genero

    def get_salario_dia(self) -> float:
        return self.__salario_dia

    def get_dias_trabajados(self) -> int:
        return self.__dias_trabajados

    def get_otros_ingresos(self) -> float:
        return self.__otros_ingresos

    def get_pagos_salud(self) -> float:
        return self.__pagos_salud

    def get_aporte_pensiones(self) -> float:
        return self.__aporte_pensiones

    def calcular_nomina(self) -> float:
        return ((self.__salario_dia * self.__dias_trabajados) +
                self.__otros_ingresos - self.__pagos_salud - self.__aporte_pensiones)


# ==========================================
# Clase: ListaEmpleados
# ==========================================
class ListaEmpleados:
    def __init__(self):
        self.lista: list[Empleado] = []
        self.total_nomina: float = 0.0

    def agregar_empleado(self, empleado: Empleado):
        self.lista.append(empleado)

    def calcular_total_nomina(self) -> float:
        self.total_nomina = 0.0
        for e in self.lista:
            self.total_nomina += e.calcular_nomina()
        return self.total_nomina

    def obtener_matriz(self) -> list[list[str]]:
        datos = []
        self.total_nomina = 0.0
        for e in self.lista:
            salario = e.calcular_nomina()
            datos.append([e.get_nombre(), e.get_apellidos(), f"{salario:.2f}"])
            self.total_nomina += salario
        return datos

    def convertir_texto(self) -> str:
        texto = ""
        for e in self.lista:
            texto += (
                f"Nombre = {e.get_nombre()}\n"
                f"Apellidos = {e.get_apellidos()}\n"
                f"Cargo = {e.get_cargo().name}\n"
                f"Género = {e.get_genero().name}\n"
                f"Salario = ${e.get_salario_dia()}\n"
                f"Días trabajados = {e.get_dias_trabajados()}\n"
                f"Otros ingresos = ${e.get_otros_ingresos()}\n"
                f"Pagos salud = ${e.get_pagos_salud()}\n"
                f"Aportes pensiones = ${e.get_aporte_pensiones()}\n"
                "---------\n"
            )
        texto += f"Total nómina = ${self.calcular_total_nomina():.2f}"
        return texto


# ==========================================
# Clase: VentanaAgregarEmpleado
# ==========================================
class VentanaAgregarEmpleado(tk.Toplevel):
    def __init__(self, master, lista: ListaEmpleados):
        super().__init__(master)
        self.lista = lista
        self.title("Agregar Empleado")
        self.geometry("300x400")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        # Nombre
        tk.Label(self, text="Nombre:").place(x=20, y=20, width=135, height=23)
        self.campo_nombre = tk.Entry(self)
        self.campo_nombre.place(x=160, y=20, width=110, height=23)

        # Apellidos
        tk.Label(self, text="Apellidos:").place(x=20, y=50, width=135, height=23)
        self.campo_apellidos = tk.Entry(self)
        self.campo_apellidos.place(x=160, y=50, width=110, height=23)

        # Cargo (Combobox)
        tk.Label(self, text="Cargo:").place(x=20, y=80, width=135, height=23)
        self.campo_cargo = ttk.Combobox(
            self,
            values=["Directivo", "Estratégico", "Operativo"],
            state="readonly"
        )
        self.campo_cargo.current(0)
        self.campo_cargo.place(x=160, y=80, width=110, height=23)

        # Género (Radiobuttons)
        tk.Label(self, text="Género:").place(x=20, y=110, width=100, height=30)
        self.var_genero = tk.StringVar(value="Masculino")
        tk.Radiobutton(self, text="Masculino", variable=self.var_genero, value="Masculino").place(x=160, y=110)
        tk.Radiobutton(self, text="Femenino", variable=self.var_genero, value="Femenino").place(x=160, y=135)

        # Salario por día
        tk.Label(self, text="Salario por día:").place(x=20, y=170, width=135, height=23)
        self.campo_salario_dia = tk.Entry(self)
        self.campo_salario_dia.place(x=160, y=170, width=110, height=23)

        # Días trabajados al mes (Spinbox)
        tk.Label(self, text="Días trabajados al mes:").place(x=20, y=200, width=135, height=23)
        self.var_dias = tk.IntVar(value=30)
        self.campo_numero_dias = tk.Spinbox(self, from_=1, to=31, textvariable=self.var_dias)
        self.campo_numero_dias.place(x=160, y=200, width=50, height=23)

        # Otros ingresos
        tk.Label(self, text="Otros ingresos:").place(x=20, y=230, width=135, height=23)
        self.campo_otros_ingresos = tk.Entry(self)
        self.campo_otros_ingresos.place(x=160, y=230, width=110, height=23)

        # Pagos por salud
        tk.Label(self, text="Pagos por salud:").place(x=20, y=260, width=135, height=23)
        self.campo_aportes_salud = tk.Entry(self)
        self.campo_aportes_salud.place(x=160, y=260, width=110, height=23)

        # Aportes pensiones
        tk.Label(self, text="Aportes pensiones:").place(x=20, y=290, width=135, height=23)
        self.campo_pensiones = tk.Entry(self)
        self.campo_pensiones.place(x=160, y=290, width=110, height=23)

        # Botones
        tk.Button(self, text="Agregar", command=self.anadir_empleado).place(x=20, y=330, width=100, height=25)
        tk.Button(self, text="Borrar", command=self.limpiar_campos).place(x=160, y=330, width=100, height=25)

    def limpiar_campos(self):
        self.campo_nombre.delete(0, tk.END)
        self.campo_apellidos.delete(0, tk.END)
        self.campo_salario_dia.delete(0, tk.END)
        self.var_dias.set(30)
        self.campo_otros_ingresos.delete(0, tk.END)
        self.campo_aportes_salud.delete(0, tk.END)
        self.campo_pensiones.delete(0, tk.END)

    def anadir_empleado(self):
        item_seleccionado = self.campo_cargo.get()
        if item_seleccionado == "Directivo":
            tipo_c = TipoCargo.DIRECTIVO
        elif item_seleccionado == "Estratégico":
            tipo_c = TipoCargo.ESTRATEGICO
        else:
            tipo_c = TipoCargo.OPERATIVO

        tipo_g = TipoGenero.MASCULINO if self.var_genero.get() == "Masculino" else TipoGenero.FEMENINO

        try:
            nombre = self.campo_nombre.get().strip()
            apellidos = self.campo_apellidos.get().strip()
            if not nombre or not apellidos:
                raise ValueError("Campos de texto vacíos")

            salario_dia = float(self.campo_salario_dia.get())
            dias_trabajados = int(self.campo_numero_dias.get())
            otros_ingresos = float(self.campo_otros_ingresos.get())
            aportes_salud = float(self.campo_aportes_salud.get())
            pensiones = float(self.campo_pensiones.get())

            empleado = Empleado(
                nombre, apellidos, tipo_c, tipo_g,
                salario_dia, dias_trabajados, otros_ingresos,
                aportes_salud, pensiones
            )
            self.lista.agregar_empleado(empleado)
            messagebox.showinfo("Mensaje", "El empleado ha sido agregado", parent=self)
            self.limpiar_campos()
        except ValueError:
            messagebox.showerror("Error", "Campo nulo o error en formato de número", parent=self)


# ==========================================
# Clase: VentanaNomina
# ==========================================
class VentanaNomina(tk.Toplevel):
    def __init__(self, master, lista: ListaEmpleados):
        super().__init__(master)
        self.lista = lista
        self.title("Nómina de Empleados")
        self.geometry("380x250")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        tk.Label(self, text="Lista de empleados:").place(x=20, y=10, width=150, height=23)

        # Tabla (Treeview)
        columnas = ("NOMBRE", "APELLIDOS", "SUELDO")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=110)

        datos = self.lista.obtener_matriz()
        for fila in datos:
            self.tabla.insert("", tk.END, values=fila)

        self.tabla.place(x=20, y=45, width=340, height=130)

        # Etiqueta de total nómina
        texto_nomina = f"Total nómina mensual = $ {self.lista.total_nomina:.2f}"
        tk.Label(self, text=texto_nomina).place(x=20, y=195, width=300, height=23)


# ==========================================
# Clase: VentanaPrincipal
# ==========================================
class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.empleados = ListaEmpleados()
        self.title("Nómina")
        self.geometry("280x380")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        barra_menu = tk.Menu(self)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)

        menu_opciones.add_command(label="Agregar empleado", command=self.abrir_agregar_empleado)
        menu_opciones.add_command(label="Calcular nómina", command=self.abrir_nomina)
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Guardar archivo", command=self.guardar_archivo)

        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.config(menu=barra_menu)

    def abrir_agregar_empleado(self):
        VentanaAgregarEmpleado(self, self.empleados)

    def abrir_nomina(self):
        VentanaNomina(self, self.empleados)

    def guardar_archivo(self):
        directorio = filedialog.askdirectory(title="Seleccionar directorio")
        if directorio:
            try:
                contenido = self.empleados.convertir_texto()
                ruta_archivo = os.path.join(directorio, "Nómina.txt")
                with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                    archivo.write(contenido)
                messagebox.showinfo(
                    "Mensaje",
                    f"El archivo de la nómina Nómina.txt se ha creado en {directorio}",
                    parent=self
                )
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}", parent=self)


# ==========================================
# Punto de entrada (Principal)
# ==========================================
if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
