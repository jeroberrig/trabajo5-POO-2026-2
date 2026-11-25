import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime


class Huesped:
    def __init__(self, nombres: str, apellidos: str, documento_identidad: int):
        self.nombres = nombres
        self.apellidos = apellidos
        self.documento_identidad = documento_identidad
        self.fecha_ingreso = None
        self.fecha_salida = None

    def set_fecha_salida(self, fecha: datetime):
        self.fecha_salida = fecha

    def set_fecha_ingreso(self, fecha: datetime):
        self.fecha_ingreso = fecha

    def get_fecha_ingreso(self) -> datetime:
        return self.fecha_ingreso

    def obtener_dias_alojamiento(self) -> int:
        diferencia = self.fecha_salida - self.fecha_ingreso
        return diferencia.days


class Habitacion:
    def __init__(self, numero_habitacion: int, disponible: bool, precio_dia: float):
        self.numero_habitacion = numero_habitacion
        self.disponible = disponible
        self.precio_dia = precio_dia
        self.huesped = None

    def get_numero_habitacion(self) -> int:
        return self.numero_habitacion

    def get_disponible(self) -> bool:
        return self.disponible

    def get_precio_dia(self) -> float:
        return self.precio_dia

    def get_huesped(self) -> Huesped:
        return self.huesped

    def set_huesped(self, huesped: Huesped):
        self.huesped = huesped

    def set_disponible(self, disponible: bool):
        self.disponible = disponible


class Hotel:
    def __init__(self):
        self.lista_habitaciones = []
        # Habitaciones 1 a 5: $120.000 | Habitaciones 6 a 10: $160.000
        for i in range(1, 11):
            precio = 120000 if i <= 5 else 160000
            self.lista_habitaciones.append(Habitacion(i, True, precio))

    def buscar_fecha_ingreso_habitacion(self, numero: int) -> str:
        for habitacion in self.lista_habitaciones:
            if habitacion.get_numero_habitacion() == numero:
                fecha = habitacion.get_huesped().get_fecha_ingreso()
                return fecha.strftime("%Y/%m/%d")
        return ""

    def buscar_habitacion_ocupada(self, numero: int) -> bool:
        for habitacion in self.lista_habitaciones:
            if habitacion.get_numero_habitacion() == numero and not habitacion.get_disponible():
                return True
        return False


class VentanaIngreso(tk.Toplevel):
    def __init__(self, master, hotel: Hotel, numero_habitacion_reservada: int):
        super().__init__(master)
        self.hotel = hotel
        self.numero_habitacion_reservada = numero_habitacion_reservada
        self.title("Ingreso")
        self.geometry("300x240")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=f"Habitación: {self.numero_habitacion_reservada}").grid(
            row=0, column=0, sticky="w", pady=3
        )

        tk.Label(frame, text="Fecha (aaaa-mm-dd):").grid(row=1, column=0, sticky="w", pady=3)
        self.campo_fecha_ingreso = tk.Entry(frame)
        self.campo_fecha_ingreso.grid(row=1, column=1, sticky="ew", pady=3)

        tk.Label(frame, text="Huésped", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky="w", pady=3
        )

        tk.Label(frame, text="Nombre:").grid(row=3, column=0, sticky="w", pady=3)
        self.campo_nombre = tk.Entry(frame)
        self.campo_nombre.grid(row=3, column=1, sticky="ew", pady=3)

        tk.Label(frame, text="Apellidos:").grid(row=4, column=0, sticky="w", pady=3)
        self.campo_apellidos = tk.Entry(frame)
        self.campo_apellidos.grid(row=4, column=1, sticky="ew", pady=3)

        tk.Label(frame, text="Doc. Identidad:").grid(row=5, column=0, sticky="w", pady=3)
        self.campo_documento = tk.Entry(frame)
        self.campo_documento.grid(row=5, column=1, sticky="ew", pady=3)

        tk.Button(frame, text="Aceptar", command=self.aceptar).grid(
            row=6, column=0, sticky="ew", padx=5, pady=10
        )
        tk.Button(frame, text="Cancelar", command=self.destroy).grid(
            row=6, column=1, sticky="ew", padx=5, pady=10
        )

        frame.columnconfigure(1, weight=1)

    def aceptar(self):
        for habitacion in self.hotel.lista_habitaciones:
            if habitacion.get_numero_habitacion() == self.numero_habitacion_reservada:
                try:
                    fecha_ingresada = self.campo_fecha_ingreso.get().strip()
                    fecha = datetime.strptime(fecha_ingresada, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror(
                        "Mensaje", "La fecha no está en el formato solicitado", parent=self
                    )
                    return

                try:
                    nombre = self.campo_nombre.get().strip()
                    apellidos = self.campo_apellidos.get().strip()
                    documento = int(self.campo_documento.get().strip())
                    if not nombre or not apellidos:
                        raise ValueError("Campos vacíos")

                    huesped = Huesped(nombre, apellidos, documento)
                    huesped.set_fecha_ingreso(fecha)
                    habitacion.set_huesped(huesped)
                    habitacion.set_disponible(False)

                    messagebox.showinfo("Mensaje", "El huésped ha sido registrado", parent=self)
                    self.destroy()
                    return
                except ValueError:
                    messagebox.showerror(
                        "Error", "Campo nulo o error en formato de número", parent=self
                    )
                    return


class VentanaHabitaciones(tk.Toplevel):
    def __init__(self, master, hotel: Hotel):
        super().__init__(master)
        self.hotel = hotel
        self.title("Habitaciones")
        self.geometry("760x260")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        # Mostrar las 10 habitaciones en 2 filas de 5
        for i, habitacion in enumerate(self.hotel.lista_habitaciones):
            fila = i // 5
            columna = i % 5
            x = 20 + columna * 140
            y = 30 + fila * 90

            tk.Label(self, text=f"Habitación {habitacion.get_numero_habitacion()}").place(
                x=x, y=y, width=130, height=23
            )
            estado = "Disponible" if habitacion.get_disponible() else "No disponible"
            tk.Label(self, text=estado).place(x=x, y=y + 20, width=100, height=23)

        tk.Label(self, text="Habitación a reservar:").place(x=230, y=180, width=140, height=23)

        self.campo_habitacion_seleccionada = tk.Spinbox(self, from_=1, to=10, width=5)
        self.campo_habitacion_seleccionada.place(x=380, y=180, width=50, height=23)

        tk.Button(self, text="Aceptar", command=self.aceptar).place(
            x=500, y=180, width=100, height=25
        )

    def aceptar(self):
        try:
            numero_habitacion = int(self.campo_habitacion_seleccionada.get())
            if numero_habitacion < 1 or numero_habitacion > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Seleccione una habitación válida (1-10)", parent=self)
            return

        if not self.hotel.buscar_habitacion_ocupada(numero_habitacion):
            self.destroy()
            VentanaIngreso(self.master, self.hotel, numero_habitacion)
        else:
            messagebox.showinfo("Mensaje", "La habitación está ocupada", parent=self)


class VentanaSalida(tk.Toplevel):
    def __init__(self, master, hotel: Hotel, numero: int):
        super().__init__(master)
        self.hotel = hotel
        self.numero_habitacion = numero
        self.habitacion_ocupada = None
        self.title("Salida huéspedes")
        self.geometry("280x260")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        frame = tk.Frame(self, padx=15, pady=10)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=f"Habitación: {self.numero_habitacion}").grid(
            row=0, column=0, sticky="w", pady=3
        )

        fecha_ingreso = self.hotel.buscar_fecha_ingreso_habitacion(self.numero_habitacion)
        tk.Label(frame, text=f"Fecha de ingreso: {fecha_ingreso}").grid(
            row=1, column=0, sticky="w", pady=3
        )

        tk.Label(frame, text="Fecha de salida (aaaa-mm-dd):").grid(
            row=2, column=0, sticky="w", pady=3
        )
        self.campo_fecha_salida = tk.Entry(frame)
        self.campo_fecha_salida.grid(row=3, column=0, sticky="ew", pady=3)

        tk.Button(frame, text="Calcular", command=self.calcular).grid(
            row=4, column=0, sticky="ew", pady=5
        )

        self.lbl_cantidad_dias = tk.Label(frame, text="Cantidad de días: ")
        self.lbl_cantidad_dias.grid(row=5, column=0, sticky="w", pady=3)

        self.lbl_total_pago = tk.Label(frame, text="Total: $")
        self.lbl_total_pago.grid(row=6, column=0, sticky="w", pady=3)

        self.btn_registrar_salida = tk.Button(
            frame, text="RegistrarSalida", command=self.registrar_salida, state="disabled"
        )
        self.btn_registrar_salida.grid(row=7, column=0, sticky="ew", pady=5)

        frame.columnconfigure(0, weight=1)

    def calcular(self):
        fecha_s = self.campo_fecha_salida.get().strip()
        for habitacion in self.hotel.lista_habitaciones:
            if habitacion.get_numero_habitacion() == self.numero_habitacion:
                self.habitacion_ocupada = habitacion
                try:
                    fecha2 = datetime.strptime(fecha_s, "%Y-%m-%d")
                    huesped = habitacion.get_huesped()
                    huesped.set_fecha_salida(fecha2)
                    fecha1 = huesped.get_fecha_ingreso()

                    if fecha1 < fecha2:
                        cantidad = huesped.obtener_dias_alojamiento()
                        self.lbl_cantidad_dias.config(text=f"Cantidad de días: {cantidad}")
                        valor = cantidad * habitacion.get_precio_dia()
                        self.lbl_total_pago.config(text=f"Total: ${valor:.2f}")
                        self.btn_registrar_salida.config(state="normal")
                    else:
                        messagebox.showerror(
                            "Mensaje",
                            "La fecha de salida es menor o igual que la de ingreso",
                            parent=self,
                        )
                except ValueError:
                    messagebox.showerror(
                        "Mensaje", "La fecha no está en el formato solicitado", parent=self
                    )
                break

    def registrar_salida(self):
        if self.habitacion_ocupada:
            self.habitacion_ocupada.set_huesped(None)
            self.habitacion_ocupada.set_disponible(True)
            messagebox.showinfo(
                "Mensaje", "Se ha registrado la salida del huésped", parent=self
            )
            self.destroy()


class VentanaPrincipal(tk.Tk):
    def __init__(self, hotel: Hotel):
        super().__init__()
        self.hotel = hotel
        self.title("Hotel")
        self.geometry("280x380")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        barra_menu = tk.Menu(self)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        menu_opciones.add_command(
            label="Consultar habitaciones", command=self.abrir_habitaciones
        )
        menu_opciones.add_command(
            label="Salida de huéspedes", command=self.abrir_salida
        )
        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.config(menu=barra_menu)

    def abrir_habitaciones(self):
        VentanaHabitaciones(self, self.hotel)

    def abrir_salida(self):
        numero_str = simpledialog.askstring(
            "Salida de huéspedes", "Ingrese número de habitación", parent=self
        )
        if numero_str is None:
            return

        try:
            numero = int(numero_str)
            if numero < 1 or numero > 10:
                messagebox.showinfo(
                    "Mensaje", "El número de habitación debe estar entre 1 y 10", parent=self
                )
            elif self.hotel.buscar_habitacion_ocupada(numero):
                VentanaSalida(self, self.hotel, numero)
            else:
                messagebox.showinfo(
                    "Mensaje", "La habitación ingresada no ha sido ocupada", parent=self
                )
        except ValueError:
            messagebox.showerror(
                "Error", "Campo nulo o error en formato de número", parent=self
            )


if __name__ == "__main__":
    hotel = Hotel()
    app = VentanaPrincipal(hotel)
    app.mainloop()
