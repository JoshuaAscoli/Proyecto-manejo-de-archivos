import tkinter as tk
from tkinter import filedialog

def open_explorer():
    # Crear una ventana de diálogo para seleccionar un archivo
    file_rute = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos GIF", "*.gif"), ("Todos los archivos", "*.*")]
    )
    
    # Mostrar la ruta del archivo seleccionado (puedes usarla según necesites)
    if file_rute:
        print(f"Archivo seleccionado: {file_rute}")
    else:
        print("No se seleccionó ningún archivo.")

    return file_rute
