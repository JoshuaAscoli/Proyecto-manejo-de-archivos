import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import time
import requests

def descargar_gif(url):
    """Descargar un archivo GIF desde una URL y guardarlo en la carpeta especificada."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la descarga falla
        
        gif_folder = get_gif_folder_path()
        gif_name = os.path.basename(url)  # Obtén el nombre del GIF desde la URL
        save_path = os.path.join(gif_folder, gif_name)
        
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        messagebox.showinfo("Descarga Completa", "El GIF ha sido descargado y guardado.")
        return save_path
    except Exception as e:
        messagebox.showerror("Error de descarga", f"No se pudo descargar el archivo: {e}")
        return None

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
        return gifs  # Retorna la lista de GIFs
    return None

def extraer_info_completa_gif(ruta_gif):
    """Extraer la información completa de un archivo GIF manualmente."""
    if not ruta_gif:
        return
    
    # Leer el archivo GIF manualmente
    with open(ruta_gif, "rb") as gif_file:
        gif_data = gif_file.read()

    # Extraer tamaño del archivo
    tamano_archivo = os.path.getsize(ruta_gif)

    # Fecha de creación y modificación
    fecha_creacion = time.ctime(os.path.getctime(ruta_gif))
    fecha_modificacion = time.ctime(os.path.getmtime(ruta_gif))

    # Identificar el encabezado del archivo GIF
    header = gif_data[:6].decode('ascii')  # Los primeros 6 bytes son el encabezado GIF87a o GIF89a
    width = int.from_bytes(gif_data[6:8], 'little')  # Ancho de la imagen en píxeles
    height = int.from_bytes(gif_data[8:10], 'little')  # Alto de la imagen en píxeles
    has_global_color_table = bool(gif_data[10] & 0b10000000)  # Bit de existencia de tabla de color global
    color_resolution = ((gif_data[10] & 0b01110000) >> 4) + 1  # Resolución del color
    frame_count = gif_data.count(b'\x2C')  # Número de imágenes (frames) identificadas por el byte \x2C

    # Crear información para mostrar en el Text widget
    info = (
        f"Archivo: {os.path.basename(ruta_gif)}\n"
        f"Tamaño del archivo: {tamano_archivo} bytes\n"
        f"Fecha de creación: {fecha_creacion}\n"
        f"Fecha de modificación: {fecha_modificacion}\n"
        f"Encabezado: {header}\n"
        f"Resolución: {width}x{height} píxeles\n"
        f"Tabla de color global: {'Sí' if has_global_color_table else 'No'}\n"
        f"Resolución del color: {color_resolution} bits\n"
        f"Frames totales: {frame_count}\n"
    )

    # Limpiar el Text widget antes de mostrar la nueva información
    text_info.delete(1.0, tk.END)  # Eliminar el contenido anterior
    text_info.insert(tk.END, info)  # Insertar la nueva información

def agregar_carpeta():
    """Crear una nueva carpeta dentro de la carpeta GIF."""
    folder_name = entry_folder_name.get()
    if folder_name:
        gif_folder = get_gif_folder_path()
        new_folder_path = os.path.join(gif_folder, folder_name)
        try:
            os.makedirs(new_folder_path)
            messagebox.showinfo("Carpeta creada", f"La carpeta '{folder_name}' ha sido creada.")
            entry_folder_name.delete(0, tk.END)  # Limpiar el cuadro de texto
        except FileExistsError:
            messagebox.showwarning("Error", f"La carpeta '{folder_name}' ya existe.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la carpeta: {e}")
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre para la carpeta.")

def agregar_gif():
    """Agregar un nuevo GIF a la carpeta GIF."""
    gif_url = entry_gif_url.get()
    if gif_url:
        ruta_gif = descargar_gif(gif_url)
        if ruta_gif:  # Solo continuar si la descarga fue exitosa
            extraer_info_completa_gif(ruta_gif)
            entry_gif_url.delete(0, tk.END)  # Limpiar el cuadro de texto
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa una URL válida para el GIF.")

def seleccionar_gif_y_extraer():
    """Seleccionar un GIF y extraer su información."""
    ruta_gif = filedialog.askopenfilename(title="Seleccionar archivo GIF", filetypes=[("Archivos GIF", "*.gif")])
    if ruta_gif:
        extraer_info_completa_gif(ruta_gif)

ventana = tk.Tk()
ventana.title("Extractor de datos de archivos GIF")
ventana.geometry("800x500")  # Aumentar la altura para el Text widget

# Cambiar el color de fondo de la ventana
ventana.configure(bg="#98FB98")  # Un verde suave (Light Green)

# Label en negrita
label_titulo = tk.Label(ventana, text="Extractor de datos de archivos GIF", font=("Arial", 16, "bold"), bg="#98FB98")
label_titulo.pack(pady=10)

# Marco para la creación de carpetas
frame_carpeta = tk.Frame(ventana, bg="#98FB98")
frame_carpeta.pack(pady=10)

tk.Label(frame_carpeta, text="Agregar Carpeta:", font=("Arial", 12), bg="#98FB98").pack(side=tk.LEFT)
entry_folder_name = tk.Entry(frame_carpeta, font=("Arial", 12))
entry_folder_name.pack(side=tk.LEFT)
tk.Button(frame_carpeta, text="Crear", command=agregar_carpeta, font=("Arial", 12)).pack(side=tk.LEFT)

# Marco para agregar GIFs
frame_gif = tk.Frame(ventana, bg="#98FB98")
frame_gif.pack(pady=10)

tk.Label(frame_gif, text="Ingresar URL de nuevo GIF:", font=("Arial", 12), bg="#98FB98").pack(side=tk.LEFT)
entry_gif_url = tk.Entry(frame_gif, font=("Arial", 12))
entry_gif_url.pack(side=tk.LEFT)
tk.Button(frame_gif, text="Agregar", command=agregar_gif, font=("Arial", 12)).pack(side=tk.LEFT)

# Botón para extraer información completa de un GIF
tk.Button(ventana, text="Extraer Información de un GIF", command=seleccionar_gif_y_extraer, font=("Arial", 12)).pack(pady=5)

# Text widget para mostrar la información del GIF
text_info = tk.Text(ventana, height=10, width=50, font=("Arial", 14))
text_info.pack(pady=10)

# Cambiar el color de fondo del Text widget
text_info.configure(bg="#E0FFE0")  # Un verde muy claro (Light Green)

# Botón para cerrar la ventana
tk.Button(ventana, text="Cerrar", command=ventana.quit, font=("Arial", 17)).pack(pady=5)

# Iniciar el programa
gifs = comprobar_gifs_en_carpeta()
if not gifs:
    url = simpledialog.askstring("Ingresar URL", "No hay GIFs en la carpeta. Por favor, ingresa el enlace del GIF:")
    if url:
        ruta_gif = descargar_gif(url)
        if ruta_gif:  # Solo continuar si la descarga fue exitosa
            extraer_info_completa_gif(ruta_gif)

ventana.mainloop()
