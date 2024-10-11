import tkinter as tk
from file_explorer import open_explorer, comprobar_gifs_en_carpeta, prompt_for_gif_url_and_download
from PIL import Image, ImageTk

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

# Función para manejar la selección del archivo GIF y animarlo
def seleccionar_y_mostrar_gif():
    ruta_gif = open_explorer()  # Obtener la ruta del archivo GIF seleccionado
    if ruta_gif:
        if hasattr(seleccionar_y_mostrar_gif, 'gif_obj'):
            # Destruir el GIF animado anterior si existe
            seleccionar_y_mostrar_gif.gif_obj.label.destroy()
        
        # Crear un nuevo objeto AnimatedGIF y reemplazar el anterior
        seleccionar_y_mostrar_gif.gif_obj = AnimatedGIF(ventana, ruta_gif)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("PROYECTO GIF")
ventana.geometry("400x400")

# Verificar si existen GIFs en la carpeta "GIF" del escritorio
if not comprobar_gifs_en_carpeta():
    prompt_for_gif_url_and_download()

# Botón para abrir el explorador de archivos y mostrar el GIF animado
boton_abrir = tk.Button(ventana, text="Abrir y Mostrar GIF Animado", command=seleccionar_y_mostrar_gif)
boton_abrir.pack(pady=20)

# Botón para cerrar la ventana
boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
boton_cerrar.pack(pady=10)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
