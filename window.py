import tkinter as tk
from file_explorer import open_explorer, comprobar_gifs_en_carpeta, prompt_for_gif_url_and_download, crear_carpeta_en_gif
from PIL import Image, ImageTk
import os
import time

class AnimatedGIF:
    def __init__(self, ventana, ruta_gif):
        self.ventana = ventana
        self.frames = self.cargar_gif(ruta_gif)
        self.label = None
        self.frame_index = 0
        self.play_animation()

    def cargar_gif(self, ruta_gif):
        """Cargar los frames del GIF usando Pillow."""
        image = Image.open(ruta_gif)
        frames = []
        try:
            while True:
                frame = ImageTk.PhotoImage(image.copy())
                frames.append(frame)
                image.seek(len(frames))  # Intentar cargar el siguiente frame
        except EOFError:
            pass  # Salimos cuando no hay más frames
        return frames

    def play_animation(self):
        """Reproducir los frames del GIF."""
        if self.label is not None:
            self.label.destroy()  # Destruir el label anterior si existe
        
        self.label = tk.Label(self.ventana)  # Crear un nuevo label para el GIF
        self.label.pack(pady=10)
        
        self.update_frame()

    def update_frame(self):
        """Actualizar el frame del GIF para crear la animación."""
        frame = self.frames[self.frame_index]
        self.label.config(image=frame)
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.ventana.after(100, self.update_frame)  # Cambiar frame cada 100 ms

def extraer_info_completa_gif(ruta_gif):
    """Extraer la información completa de un archivo GIF."""
    if not ruta_gif:
        return
    
    # Abrir el GIF usando Pillow
    gif_image = Image.open(ruta_gif)

    # Tamaño de la imagen
    ancho, alto = gif_image.size

    # Versión del GIF (87a o 89a)
    version = gif_image.info.get('version', 'Desconocida')

    # Color de fondo (si existe)
    color_fondo = gif_image.info.get('background', 'No especificado')

    # Cantidad de colores (si tiene tabla de colores global)
    cantidad_colores = len(gif_image.getpalette()) // 3 if gif_image.getpalette() else 'No especificado'

    # Cantidad de imágenes (frames)
    cantidad_imagenes = gif_image.n_frames

    # Fechas de creación y modificación
    fecha_creacion = time.ctime(os.path.getctime(ruta_gif))
    fecha_modificacion = time.ctime(os.path.getmtime(ruta_gif))

    # Comentarios (si existen)
    comentarios = gif_image.info.get('comment', 'No hay comentarios')

    # Mostrar la información en un cuadro de mensaje
    info = (
        f"Archivo: {os.path.basename(ruta_gif)}\n"
        f"Versión GIF: {version}\n"
        f"Tamaño de imagen: {ancho}x{alto} píxeles\n"
        f"Cantidad de colores: {cantidad_colores}\n"
        f"Color de fondo: {color_fondo}\n"
        f"Cantidad de imágenes: {cantidad_imagenes}\n"
        f"Fecha de creación: {fecha_creacion}\n"
        f"Fecha de modificación: {fecha_modificacion}\n"
        f"Comentarios: {comentarios}\n"
    )

    tk.messagebox.showinfo("Información completa del GIF", info)

# Función para manejar la selección del archivo GIF y animarlo
def seleccionar_y_mostrar_gif():
    ruta_gif = open_explorer()  # Obtener la ruta del archivo GIF seleccionado
    if ruta_gif:
        if hasattr(seleccionar_y_mostrar_gif, 'gif_obj'):
            # Destruir el GIF animado anterior si existe
            seleccionar_y_mostrar_gif.gif_obj.label.destroy()
        
        # Crear un nuevo objeto AnimatedGIF y reemplazar el anterior
        seleccionar_y_mostrar_gif.gif_obj = AnimatedGIF(ventana, ruta_gif)

# Función para mostrar la información del GIF seleccionado
def mostrar_info_gif():
    ruta_gif = open_explorer()  # Obtener la ruta del archivo GIF seleccionado
    if ruta_gif:
        extraer_info_completa_gif(ruta_gif)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("PROYECTO GIF")
ventana.geometry("400x400")

# Verificar si existen GIFs en la carpeta "GIF" del escritorio
if not comprobar_gifs_en_carpeta():
    prompt_for_gif_url_and_download()

# Botón para abrir el explorador de archivos y mostrar el GIF animado
boton_abrir = tk.Button(ventana, text="Abrir y Mostrar GIF Animado", command=seleccionar_y_mostrar_gif)
boton_abrir.pack(pady=1)

# Botón para mostrar la información del GIF seleccionado
boton_info = tk.Button(ventana, text="Ver información de GIF", command=mostrar_info_gif)
boton_info.pack(pady=1)

# Botón para crear una nueva carpeta dentro de la carpeta GIF
boton_crear_carpeta = tk.Button(ventana, text="Crear nueva carpeta en GIF", command=crear_carpeta_en_gif)
boton_crear_carpeta.pack(pady=1)

# Botón para cerrar la ventana
boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
boton_cerrar.pack(pady=1)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
