# Calculadora de rentabilidad V2

UI moderna hecha con CustomTkinter.

## Instalar dependencias

```powershell
# Opcional: crear entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias de V2
pip install -r V2/requirements.txt
```

## Ejecutar en desarrollo

```powershell
python V2\calculadora_rentabilidad_desktop_V2.py
```

## Generar .exe con PyInstaller

```powershell
# Instalar PyInstaller si no lo tienes
pip install pyinstaller

# Compilar .exe (modo ventana, sin consola)
pyinstaller --noconfirm --clean --onefile --windowed --name CalculadoraRentabilidadV2 V2\calculadora_rentabilidad_desktop_V2.py
```

- El ejecutable aparecerá en `dist/CalculadoraRentabilidadV2.exe`.
- Si quieres un icono, añade `--icon ruta\a\icono.ico`.

## Fórmulas
- Precio de impresión = `B1 * (B2 / 1000)`
- Precio recomendado de venta = `((B1*(B2/1000) + B3 + 0.1) * (1 + B4)) * (1 + 0.4 * B5)`

Notas:
- Campos aceptan coma o punto para decimales.
- “Precio recomendado de venta” se muestra sin redondeo, como pediste.
