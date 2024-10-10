import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os

CONFIG_FILE = 'config.txt'

def get_saved_path():
    """Obtener la ruta guardada desde el archivo de configuración."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return file.read().strip()
    return None

def save_path(path):
    """Guardar la ruta en el archivo de configuración."""
    with open(CONFIG_FILE, 'w') as file:
        file.write(path)

def prompt_for_path():
    """Mostrar un cuadro de diálogo para que el usuario ingrese una ruta."""
    path = simpledialog.askstring("Ruta de archivo", "Por favor, ingrese la ruta del archivo:")
    if path:
        save_path(path)
        messagebox.showinfo("Éxito", f"Ruta guardada: {path}")
        print(f"Ruta guardada: {path}")
    else:
        messagebox.showwarning("Advertencia", "No se ingresó ninguna ruta.")
        print("No se ingresó ninguna ruta.")

def open_explorer():
    """Abrir el explorador de archivos para seleccionar un archivo."""
    file_rute = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos GIF", "*.gif"), ("Todos los archivos", "*.*")]
    )
    
    if file_rute:
        print(f"Archivo seleccionado: {file_rute}")
    else:
        print("No se seleccionó ningún archivo.")
    
    return file_rute
