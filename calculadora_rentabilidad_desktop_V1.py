#!/usr/bin/env python3
"""
Calculadora de rentabilidad - versión escritorio (Tkinter)
Recrea las fórmulas de tu Excel actualizadas:

Precio de impresión (solo coste de material):
    B1 * (B2 / 1000)

Precio recomendado de venta:
    ((B1*(B2/1000) + B3 + 0.1) * (1 + B4)) * (1 + 0.4 * B5)

Cómo usar:
- Ejecuta: python Calculadora_rentabilidad_desktop.py
- Requiere Python 3.8+ (Tkinter viene por defecto en la mayoría de instalaciones).
- Para crear un .exe usa pyinstaller si quieres: `pyinstaller --onefile Calculadora_rentabilidad_desktop.py`

Interfaz:
- Inserta: precio por kg (B1), peso en gramos (B2), gastos extra (B3), beneficio (%) y impuesto mecanizado (%)
- El programa muestra: Precio de impresión y Precio recomendado de venta

Autor: Generado por ChatGPT
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def calcular(precio_kg, peso_g, gastos_extra, beneficio_pct, impuesto_pct):
    # Convertir porcentajes a factores
    def convertir_numero(valor, nombre_campo, obligatorio=True):
        """Convierte string a float, acepta coma como separador decimal"""
        valor = str(valor).strip().replace(',', '.')
        if not valor:
            if obligatorio:
                raise ValueError(f"{nombre_campo} es obligatorio.")
            return 0.0
        try:
            return float(valor)
        except ValueError:
            raise ValueError(f"{nombre_campo} no es un número válido.")
    
    try:
        B1 = convertir_numero(precio_kg, "Precio kg de PLA", obligatorio=True)
        B2 = convertir_numero(peso_g, "Peso del encargo", obligatorio=True)
        B3 = convertir_numero(gastos_extra, "Gastos extra", obligatorio=False)
        # beneficio_pct en porcentaje (ej: 10 -> 10%)
        B4 = convertir_numero(beneficio_pct, "Beneficio", obligatorio=False) / 100.0
        B5 = convertir_numero(impuesto_pct, "Impuesto mecanizado", obligatorio=False) / 100.0
    except Exception as e:
        raise ValueError(str(e))

    # Precio de impresión: solo material
    precio_impresion = B1 * (B2 / 1000.0)

    # Precio recomendado de venta (mantiene la fórmula original para venta)
    base_cost = (precio_impresion + B3 + 0.1)  # incluye el +0.1 fijo
    with_benefit = base_cost * (1 + B4)
    precio_venta = with_benefit * (1 + 0.4 * B5)

    # Mostrar sin redondear el precio recomendado de venta
    precio_venta_mostrado = precio_venta

    return precio_impresion, precio_venta, precio_venta_mostrado


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de rentabilidad - DTLI")
        self.resizable(False, False)
        self._build_ui()
        # Ajustar tamaño a contenido
        self.update_idletasks()
        self.geometry(f"{self.winfo_reqwidth()}x{self.winfo_reqheight()}")

    def _build_ui(self):
        pad = {'padx': 8, 'pady': 6}

        frm = ttk.Frame(self)
        frm.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Entradas
        labels = [
            ("Precio kg de PLA (€):", "0"),
            ("Peso del encargo (g):", "0"),
            ("Gastos extra (€):", "0"),
            ("Beneficio (%):", "0"),
            ("Impuesto mecanizado (%):", "0"),
        ]

        self.entries = {}
        for i, (text, default) in enumerate(labels):
            lbl = ttk.Label(frm, text=text)
            lbl.grid(row=i, column=0, sticky=tk.W, **pad)
            ent = ttk.Entry(frm)
            ent.insert(0, default)
            ent.grid(row=i, column=1, sticky=tk.EW, **pad)
            self.entries[text] = ent

        # Botón calcular
        btn = ttk.Button(frm, text="Calcular", command=self.on_calcular)
        btn.grid(row=5, column=0, columnspan=2, sticky=tk.EW, **pad)

        # Resultados
        sep = ttk.Separator(frm, orient='horizontal')
        sep.grid(row=6, column=0, columnspan=2, sticky='ew', pady=(6, 6))

        self.result_precio_lbl = ttk.Label(frm, text="Precio de impresión: — €")
        self.result_precio_lbl.grid(row=7, column=0, columnspan=2, sticky=tk.W, **pad)

        self.result_precio_red_lbl = ttk.Label(frm, text="Precio recomendado de venta: — €")
        self.result_precio_red_lbl.grid(row=8, column=0, columnspan=2, sticky=tk.W, **pad)

        # (Se elimina la etiqueta de fórmula en el pie de página por solicitud)

        # Expand column 1 for entries
        frm.columnconfigure(1, weight=1)

    def on_calcular(self):
        try:
            precio_kg = self.entries["Precio kg de PLA (€):"].get()
            peso_g = self.entries["Peso del encargo (g):"].get()
            gastos_extra = self.entries["Gastos extra (€):"].get()
            beneficio = self.entries["Beneficio (%):"].get()
            impuesto = self.entries["Impuesto mecanizado (%):"].get()
            precio_imp, precio_venta, precio_venta_mostrado = calcular(precio_kg, peso_g, gastos_extra, beneficio, impuesto)

            self.result_precio_lbl.config(text=f"Precio de impresión: {precio_imp:.4f} €")
            # Mostrar el precio recomendado de venta con todos los decimales (sin redondeo)
            self.result_precio_red_lbl.config(text=f"Precio recomendado de venta: {precio_venta_mostrado} €")

        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")


if __name__ == '__main__':
    app = App()
    app.mainloop()
