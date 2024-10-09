import tkinter as tk
# Ventana de incio 
# Crear la ventana principal
ventana = tk.Tk()
ventana.title("PROYECTO GIF") 
ventana.geometry("400x300")  

# Botón para cerrar ventana
boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
boton_cerrar.pack(pady=10)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
