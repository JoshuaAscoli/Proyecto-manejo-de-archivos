import tkinter as tk
from file_explorer import open_explorer  # Importar la función del archivo externo

# Ventana de inicio 
# Crear la ventana principal
ventana = tk.Tk()
ventana.title("PROYECTO GIF") 
ventana.geometry("400x300")  

# Botón para abrir el explorador de archivos
boton_abrir = tk.Button(ventana, text="Abrir Explorador de Archivos", command=open_explorer )
boton_abrir.pack(pady=20)

# Botón para cerrar ventana
boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
boton_cerrar.pack(pady=10)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
