import tkinter as tk
from tkinter import messagebox
from pynput import mouse
import threading
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import os

# Variables globales
tracking = False
mouse_listener = None
activity_name = ""
origin = (0, 0)
log_data = []
clicks = []
start_time = None
end_time = None

# Función para graficar y guardar imagen
def plot_trajectory_and_save():
    if not log_data:
        return

    xs, ys = zip(*[(x, y) for _, _, x, y in log_data])
    cx, cy = zip(*clicks) if clicks else ([], [])

    plt.figure(figsize=(15, 15))
    plt.plot(xs, ys, label="Trayectoria", color="blue")
    if clicks:
        plt.scatter(cx, cy, color="red", marker='x', label="Clics")

    plt.title(f"Actividad: {activity_name}\nDuración: {round(end_time - start_time, 2)} segundos")
    plt.xlabel("ΔX")
    plt.ylabel("ΔY")
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='gray', lw=0.5)
    plt.axvline(0, color='gray', lw=0.5)

    # Crear carpeta si no existe
    os.makedirs("Trajectories", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Trajectories/{activity_name}_{timestamp}_{int(end_time - start_time)}s.png"
    plt.savefig(filename)
    plt.close()
    print(f"Imagen guardada como: {filename}")

# Guardar CSV si se desea
def save_csv():
    if log_data:
        filename = f"{activity_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Actividad", "Tiempo", "Rel_X", "Rel_Y"])
            writer.writerows(log_data)
        print(f"Datos guardados en {filename}")

# Evento de movimiento
def on_move(x, y):
    if tracking:
        dx = x - origin[0]
        dy = y - origin[1]
        log_data.append([activity_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), dx, dy])

# Evento de clic
def on_click(x, y, button, pressed):
    if tracking and pressed:
        dx = x - origin[0]
        dy = y - origin[1]
        clicks.append((dx, dy))

# Inicio del rastreo con delay
def delayed_start():
    global tracking, mouse_listener, origin, log_data, clicks, start_time

    time.sleep(5)
    origin = mouse.Controller().position
    log_data = []
    clicks = []
    tracking = True
    start_time = time.time()

    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    mouse_listener.start()
    status_label.config(text="Rastreando...", fg="green")

# Botón: iniciar
def start_tracking():
    global tracking, activity_name

    if tracking:
        messagebox.showwarning("Ya activo", "El rastreo ya está en curso.")
        return

    activity_name = activity_entry.get().strip().replace(" ", "_")
    if not activity_name:
        messagebox.showwarning("Actividad requerida", "Ingresa una actividad antes de iniciar.")
        return

    status_label.config(text="Esperando (5s)...", fg="orange")
    threading.Thread(target=delayed_start, daemon=True).start()

# Botón: detener
def stop_tracking():
    global tracking, mouse_listener, end_time

    if not tracking:
        messagebox.showinfo("No rastreando", "El rastreo no está activo.")
        return

    tracking = False
    end_time = time.time()

    if mouse_listener:
        mouse_listener.stop()
        mouse_listener = None

    status_label.config(text="Inactivo", fg="red")
    plot_trajectory_and_save()
    save_csv()

# Interfaz gráfica
root = tk.Tk()
root.title("Rastreador de Trayectorias del Mouse")

tk.Label(root, text="Actividad:").pack(pady=5)
activity_entry = tk.Entry(root, width=40)
activity_entry.pack(pady=5)

start_button = tk.Button(root, text="Iniciar Rastreo", command=start_tracking, bg="lightgreen")
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Detener Rastreo", command=stop_tracking, bg="tomato")
stop_button.pack(pady=5)

status_label = tk.Label(root, text="Inactivo", fg="red", font=("Arial", 12, "bold"))
status_label.pack(pady=10)

root.mainloop()
# Cierre de la aplicación