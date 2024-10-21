import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import requests

def get_gif_folder_path():
    """Obtener la ruta de la carpeta GIF en el escritorio."""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "GIF")
    if os.path.exists(desktop_path):
        return desktop_path
    else:
        messagebox.showerror("Error", "La carpeta 'GIF' no existe en el escritorio.")
        return None

def comprobar_gifs_en_carpeta():
    """Verificar si existen GIFs en la carpeta GIF del escritorio."""
    gif_folder = get_gif_folder_path()
    if gif_folder:
        gifs = [f for f in os.listdir(gif_folder) if f.endswith('.gif')]
        if gifs:
            return True  # Si hay archivos GIF, retornar True
        else:
            return False  # Si no hay archivos GIF, retornar False
    return None

def descargar_gif(url, save_path):
    """Descargar un archivo GIF desde una URL y guardarlo en la carpeta especificada."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la descarga falla
        with open(save_path, 'wb') as file:
            file.write(response.content)
        messagebox.showinfo("Descarga Completa", "El GIF ha sido descargado y guardado.")
    except Exception as e:
        messagebox.showerror("Error de descarga", f"No se pudo descargar el archivo: {e}")

def prompt_for_gif_url_and_download():
    """Solicitar al usuario el enlace del GIF y descargarlo en la carpeta GIF."""
    gif_folder = get_gif_folder_path()
    if gif_folder:
        url = simpledialog.askstring("Ingresar URL", "Por favor, ingresa el enlace del primer archivo GIF:")
        if url:
            gif_name = os.path.basename(url)
            save_path = os.path.join(gif_folder, gif_name)
            descargar_gif(url, save_path)

def open_explorer():
    """Abrir el explorador de archivos, restringido a la carpeta GIF en el escritorio."""
    gif_folder = get_gif_folder_path()
    
    if gif_folder:
        file_rute = filedialog.askopenfilename(
            initialdir=gif_folder,
            title="Seleccionar archivo",
            filetypes=[("Archivos GIF", "*.gif"), ("Todos los archivos", "*.*")]
        )
        
        if file_rute:
            return file_rute
    return None

def crear_carpeta_en_gif():
    """Crear una nueva carpeta dentro de la carpeta GIF en el escritorio."""
    gif_folder = get_gif_folder_path()
    if gif_folder:
        nueva_carpeta = simpledialog.askstring("Nombre de la carpeta", "Introduce el nombre de la nueva carpeta:")
        if nueva_carpeta:
            nueva_ruta = os.path.join(gif_folder, nueva_carpeta)
            try:
                os.makedirs(nueva_ruta)
                messagebox.showinfo("Carpeta creada", f"La carpeta '{nueva_carpeta}' ha sido creada.")
            except Exception as e:
                messagebox.showerror("Error al crear la carpeta", f"No se pudo crear la carpeta: {e}")
