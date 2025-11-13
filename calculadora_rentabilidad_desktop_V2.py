#!/usr/bin/env python3
"""
Calculadora de rentabilidad V2 (CustomTkinter)

Cambios clave V2:
- UI moderna con CustomTkinter (temas claro/oscuro, tarjetas de resultados)
- Cálculo en vivo y botón Copiar
- Ventana se ajusta al contenido y se centra

Fórmulas:
- Precio de impresión: B1 * (B2 / 1000)
- Precio recomendado de venta: ((B1*(B2/1000) + B3 + 0.1) * (1 + B4)) * (1 + 0.4 * B5)

Cómo ejecutar:
- python V2/calculadora_rentabilidad_desktop_V2.py

Para generar .exe (PyInstaller ejemplo):
- pyinstaller --noconfirm --clean --onefile --windowed --name CalculadoraRentabilidadV2 V2/calculadora_rentabilidad_desktop_V2.py
"""

import sys
import math
import tkinter as tk
import customtkinter as ctk


def convertir_numero(valor: str, obligatorio: bool = True) -> float:
    """Convierte string a float, acepta coma como separador decimal."""
    s = str(valor).strip().replace(',', '.')
    if not s:
        if obligatorio:
            raise ValueError("Este campo es obligatorio.")
        return 0.0
    try:
        return float(s)
    except Exception:
        raise ValueError("Número no válido.")


def calcular(precio_kg: str, peso_g: str, gastos_extra: str, beneficio_pct: str, impuesto_pct: str):
    # Entradas sanitizadas
    B1 = convertir_numero(precio_kg, obligatorio=True)
    B2 = convertir_numero(peso_g, obligatorio=True)
    B3 = convertir_numero(gastos_extra, obligatorio=False)
    B4 = convertir_numero(beneficio_pct, obligatorio=False) / 100.0
    B5 = convertir_numero(impuesto_pct, obligatorio=False) / 100.0

    precio_impresion = B1 * (B2 / 1000.0)
    base_cost = precio_impresion + B3 + 0.1
    with_benefit = base_cost * (1 + B4)
    precio_venta = with_benefit * (1 + 0.4 * B5)

    return precio_impresion, precio_venta


class ResultCard(ctk.CTkFrame):
    def __init__(self, master, title: str):
        super().__init__(master)
        self._title = title
        self.columnconfigure(0, weight=1)
        self.label_title = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=14, weight="bold"))
        self.label_title.grid(row=0, column=0, sticky="w", padx=12, pady=(10, 0))
        self.value_var = tk.StringVar(value="— €")
        self.label_value = ctk.CTkLabel(self, textvariable=self.value_var, font=ctk.CTkFont(size=22, weight="bold"))
        self.label_value.grid(row=1, column=0, sticky="w", padx=12, pady=(4, 10))

        self.copy_btn = ctk.CTkButton(self, text="Copiar", width=90, command=self._copy)
        self.copy_btn.grid(row=1, column=1, sticky="e", padx=12, pady=(4, 10))

    def set_value(self, value_text: str):
        self.value_var.set(value_text)

    def _copy(self):
        val = self.value_var.get().replace(' €', '')
        self.clipboard_clear()
        self.clipboard_append(val)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de rentabilidad - V2")

        # Apariencia
        ctk.set_appearance_mode("system")  # "light" | "dark" | "system"
        ctk.set_default_color_theme("blue")

        # Layout principal
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_header()
        self._build_content()
        self._build_footer()

        # Ajustar tamaño a contenido y centrar (tras primer layout)
        self.after_idle(self._finalize_window)

    def _build_header(self):
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 0))
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(header, text="Calculadora de rentabilidad", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, sticky="w", padx=10, pady=8)

        self.theme_switch = ctk.CTkSegmentedButton(header, values=["Sistema", "Claro", "Oscuro"],
                                                   command=self._on_theme_change)
        self.theme_switch.set("Sistema")
        self.theme_switch.grid(row=0, column=1, sticky="e", padx=10, pady=8)

    def _build_content(self):
        # Panel de entradas (izquierda)
        left = ctk.CTkFrame(self)
        left.grid(row=1, column=0, sticky="nsew", padx=(10, 6), pady=10)
        left.grid_columnconfigure(1, weight=1)

        self.inputs = {}
        fields = [
            ("Precio kg de PLA (€)", "0"),
            ("Peso del encargo (g)", "0"),
            ("Gastos extra (€)", "0"),
            ("Beneficio (%)", "0"),
            ("Impuesto mecanizado (%)", "0"),
        ]

        for i, (label, default) in enumerate(fields):
            lbl = ctk.CTkLabel(left, text=label)
            lbl.grid(row=i, column=0, sticky="w", padx=10, pady=(8 if i == 0 else 4, 2))
            ent = ctk.CTkEntry(left, placeholder_text=default)
            ent.insert(0, default)
            ent.grid(row=i, column=1, sticky="ew", padx=10, pady=(8 if i == 0 else 4, 2))
            ent.bind("<KeyRelease>", self._on_change)
            self.inputs[label] = ent

        # Botón calcular
        self.calc_btn = ctk.CTkButton(left, text="Calcular", command=self._calculate_and_update)
        self.calc_btn.grid(row=len(fields), column=0, columnspan=2, sticky="ew", padx=10, pady=(12, 10))

        # Panel de resultados (derecha)
        right = ctk.CTkFrame(self)
        right.grid(row=1, column=1, sticky="nsew", padx=(6, 10), pady=10)
        right.grid_columnconfigure(0, weight=1)

        self.card_impresion = ResultCard(right, "Precio de impresión")
        self.card_impresion.grid(row=0, column=0, sticky="ew", padx=8, pady=(10, 6))

        self.card_venta = ResultCard(right, "Precio recomendado de venta")
        self.card_venta.grid(row=1, column=0, sticky="ew", padx=8, pady=(6, 10))

    def _build_footer(self):
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 8))
        footer.grid_columnconfigure(0, weight=1)
        copyright_label = ctk.CTkLabel(
            footer,
            text="© 2025 Daftical56 (idea) · CarlosIn120FPS (execution)",
            font=ctk.CTkFont(size=11)
        )
        copyright_label.grid(row=0, column=0, sticky="e")

    def _finalize_window(self):
        if not self.winfo_exists():
            return
        try:
            self.update_idletasks()
            self.geometry(f"{self.winfo_reqwidth()}x{self.winfo_reqheight()}")
            # Centrar ventana
            w = self.winfo_width()
            h = self.winfo_height()
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            x = int((sw - w) / 2)
            y = int((sh - h) / 3)
            self.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass

    def _on_theme_change(self, value: str):
        if value == "Claro":
            ctk.set_appearance_mode("light")
        elif value == "Oscuro":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("system")

    def _on_change(self, _event=None):
        # Cálculo en vivo con silencioso ante errores
        try:
            self._calculate_and_update()
        except Exception:
            pass

    def _calculate_and_update(self):
        try:
            precio_kg = self.inputs["Precio kg de PLA (€)"].get()
            peso_g = self.inputs["Peso del encargo (g)"].get()
            gastos_extra = self.inputs["Gastos extra (€)"].get()
            beneficio = self.inputs["Beneficio (%)"].get()
            impuesto = self.inputs["Impuesto mecanizado (%)"].get()

            p_imp, p_venta = calcular(precio_kg, peso_g, gastos_extra, beneficio, impuesto)

            # Mostrar según requisitos: impresión a 4 decimales, venta sin redondeo
            self.card_impresion.set_value(f"{p_imp:.4f} €")
            self.card_venta.set_value(f"{p_venta} €")
        except Exception as e:
            # Mostrar indicadores vacíos si hay error, sin interrumpir la edición
            self.card_impresion.set_value("— €")
            self.card_venta.set_value("— €")


if __name__ == "__main__":
    app = App()
    app.mainloop()
