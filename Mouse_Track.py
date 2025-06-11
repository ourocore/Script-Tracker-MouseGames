import tkinter as tk
from tkinter import messagebox
from pynput import mouse
import threading
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import os

class MouseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rastreador de Trayectorias del Mouse")

        # Estados internos
        self.tracking = False
        self.listener = None
        self.activity_name = ""
        self.origin = (0, 0)
        self.log_data = []
        self.clicks = []
        self.start_time = None
        self.end_time = None

        self.build_gui()

    def build_gui(self):
        tk.Label(self.root, text="Actividad:").pack(pady=5)
        self.activity_entry = tk.Entry(self.root, width=40)
        self.activity_entry.pack(pady=5)

        tk.Button(self.root, text="Iniciar Rastreo", command=self.start_tracking, bg="lightgreen").pack(pady=5)
        tk.Button(self.root, text="Detener Rastreo", command=self.stop_tracking, bg="tomato").pack(pady=5)

        self.status_label = tk.Label(self.root, text="Inactivo", fg="red", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=10)

    def start_tracking(self):
        if self.tracking:
            messagebox.showwarning("Ya activo", "El rastreo ya está en curso.")
            return

        self.activity_name = self.activity_entry.get().strip().replace(" ", "_")
        if not self.activity_name:
            messagebox.showwarning("Actividad requerida", "Ingresa una actividad antes de iniciar.")
            return

        self.status_label.config(text="Esperando (5s)...", fg="orange")
        threading.Thread(target=self._delayed_start, daemon=True).start()

    def _delayed_start(self):
        time.sleep(5)
        self.origin = mouse.Controller().position
        self.log_data.clear()
        self.clicks.clear()
        self.start_time = time.time()
        self.tracking = True

        self.listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        self.listener.start()
        self.status_label.config(text="Rastreando...", fg="green")

    def stop_tracking(self):
        if not self.tracking:
            messagebox.showinfo("No rastreando", "El rastreo no está activo.")
            return

        self.tracking = False
        self.end_time = time.time()

        if self.listener:
            self.listener.stop()
            self.listener = None

        self.status_label.config(text="Inactivo", fg="red")

        self.plot_and_save()
        self.save_csv()

    def on_move(self, x, y):
        if self.tracking:
            dx = x - self.origin[0]
            dy = y - self.origin[1]
            self.log_data.append([self.activity_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), dx, dy])

    def on_click(self, x, y, button, pressed):
        if self.tracking and pressed:
            dx = x - self.origin[0]
            dy = y - self.origin[1]
            self.clicks.append((dx, dy))

    def plot_and_save(self):
        if not self.log_data:
            return

        xs, ys = zip(*[(x, y) for _, _, x, y in self.log_data])
        cx, cy = zip(*self.clicks) if self.clicks else ([], [])

        plt.figure(figsize=(15, 15))
        plt.plot(xs, ys, label="Trayectoria", color="blue")
        if self.clicks:
            plt.scatter(cx, cy, color="red", marker='x', label="Clics")

        duration = round(self.end_time - self.start_time, 2)
        plt.title(f"Actividad: {self.activity_name}\nDuración: {duration} segundos")
        plt.xlabel("ΔX")
        plt.ylabel("ΔY")
        plt.legend()
        plt.grid(True)
        plt.axhline(0, color='gray', lw=0.5)
        plt.axvline(0, color='gray', lw=0.5)

        os.makedirs("Trajectories", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Trajectories/{self.activity_name}_{timestamp}_{int(duration)}s.png"
        plt.savefig(filename)
        plt.close()
        print(f"Imagen guardada como: {filename}")

    def save_csv(self):
        if not self.log_data:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"Trajectories/{self.activity_name}_{timestamp}.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Actividad", "Tiempo", "Rel_X", "Rel_Y"])
            writer.writerows(self.log_data)
        print(f"Datos guardados en {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MouseTrackerApp(root)
    root.mainloop()
