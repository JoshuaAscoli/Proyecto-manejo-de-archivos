import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import time
import requests


def get_gif_folder_path():
    """Obtener la ruta de la carpeta GIF en el escritorio y crearla si no existe."""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "GIF")
    
    # Si la carpeta no existe, crearla
    if not os.path.exists(desktop_path):
        try:
            os.makedirs(desktop_path)
            messagebox.showinfo("Carpeta creada", "La carpeta 'GIF' ha sido creada en el escritorio.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la carpeta: {e}")
    
    return desktop_path  # Retorna la ruta de la carpeta GIF

def comprobar_gifs_en_carpeta():
    """Verificar si existen GIFs en la carpeta GIF del escritorio."""
    gif_folder = get_gif_folder_path()
    if gif_folder:
        gifs = [f for f in os.listdir(gif_folder) if f.endswith('.gif')]
        return gifs  # Retorna la lista de GIFs
    return None

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
        messagebox.showerror("Error de descarga", f"No se pudo descargar el archivo. Intenta con otro enlace: {e}")
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

    # Mostrar el botón para guardar información
    btn_guardar_info.pack(pady=5)

def guardar_info_en_txt(info):
    """Guardar la información extraída del GIF en un archivo de texto, agregando al inicio."""
    gif_folder = get_gif_folder_path()
    if gif_folder:
        txt_file_path = os.path.join(gif_folder, "info_gifs.txt")
        try:
            # Leer el contenido existente del archivo
            if os.path.exists(txt_file_path):
                with open(txt_file_path, 'r') as txt_file:
                    existing_content = txt_file.read()
            else:
                existing_content = ""  # Si el archivo no existe, inicializar como cadena vacía
            
            # Agregar la nueva información al inicio
            new_content = info + "\n" + "-" * 40 + "\n" + existing_content
            
            # Escribir todo el contenido de vuelta en el archivo
            with open(txt_file_path, 'w') as txt_file:  # 'w' para sobrescribir
                txt_file.write(new_content)

            messagebox.showinfo("Guardado", "La información ha sido guardada en 'info_gifs.txt'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la información en el archivo: {e}")

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
    """Seleccionar un GIF y extraer su información, abriendo la carpeta GIF."""
    gif_folder = get_gif_folder_path()  # Obtener la ruta de la carpeta GIF
    
        
    # Abrir el cuadro de diálogo para seleccionar el GIF
    ruta_gif = filedialog.askopenfilename(title="Seleccionar archivo GIF", filetypes=[("Archivos GIF", "*.gif")])
    if ruta_gif:
        extraer_info_completa_gif(ruta_gif)  # Extraer información del GIF seleccionado



def editar_info_gifs():
    """Abrir el archivo de texto para editar la información de los GIFs."""
    gif_folder = get_gif_folder_path()
    if gif_folder:
        txt_file_path = os.path.join(gif_folder, "info_gifs.txt")
        if os.path.exists(txt_file_path):
            os.startfile(txt_file_path)  # Abrir el archivo con el editor de texto predeterminado
        else:
            messagebox.showerror("Error", "El archivo 'info_gifs.txt' no existe.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Extractor de datos de archivos GIF")
ventana.geometry("800x525")  # Aumentar la altura para el Text widget

color = '#6495ED'
# Cambiar el color de fondo de la ventana
ventana.configure(bg=color)

# Label en negrita
label_titulo = tk.Label(ventana, text="Extractor de datos de archivos GIF", font=("Arial", 16, "bold"), bg=color)
label_titulo.pack(pady=10)

# Verificar la carpeta GIF al iniciar el programa
get_gif_folder_path()

# Marco para la creación de carpetas
frame_carpeta = tk.Frame(ventana, bg=color)
frame_carpeta.pack(pady=10)

tk.Label(frame_carpeta, text="Agregar Carpeta:", font=("Arial", 12), bg=color).pack(side=tk.LEFT)
entry_folder_name = tk.Entry(frame_carpeta)
entry_folder_name.pack(side=tk.LEFT)
btn_agregar_carpeta = tk.Button(frame_carpeta, text="Crear Carpeta", command=agregar_carpeta)
btn_agregar_carpeta.pack(side=tk.LEFT)

# Marco para agregar GIFs
frame_gif = tk.Frame(ventana, bg=color)
frame_gif.pack(pady=10)

tk.Label(frame_gif, text="Agregar GIF desde URL:", font=("Arial", 12), bg=color).pack(side=tk.LEFT)
entry_gif_url = tk.Entry(frame_gif)
entry_gif_url.pack(side=tk.LEFT)
btn_agregar_gif = tk.Button(frame_gif, text="Agregar GIF", command=agregar_gif)
btn_agregar_gif.pack(side=tk.LEFT)

# Botón para seleccionar GIF y extraer información
btn_seleccionar_gif = tk.Button(ventana, text="Extraer Información ", command=seleccionar_gif_y_extraer)
btn_seleccionar_gif.pack(pady=10)

# Botón para editar la información de los GIFs
btn_editar_info = tk.Button(ventana, text="Editar Información", command=editar_info_gifs)
btn_editar_info.pack(pady=10)

# Widget Text para mostrar información
text_info = tk.Text(ventana, height=10, width=80)
text_info.pack(pady=10)

# Botón para guardar información en un archivo de texto
btn_guardar_info = tk.Button(ventana, text="Guardar Información", command=lambda: guardar_info_en_txt(text_info.get(1.0, tk.END)))
btn_guardar_info.pack(pady=5)
btn_guardar_info.pack_forget()  # Ocultar el botón inicialmente

btn_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
btn_cerrar.pack(pady=5)

# Iniciar la aplicación
ventana.mainloop()
