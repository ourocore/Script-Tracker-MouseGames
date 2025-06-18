# Rastreador de Trayectorias del Mouse

Este script de Python es una aplicación de escritorio sencilla que te permite **rastrear y visualizar la trayectoria del cursor del mouse**, así como registrar los clics, durante una actividad específica. Genera gráficos de la trayectoria y guarda los datos en archivos CSV y las imágenes en PNG para su posterior análisis.

---
## Características

* **Rastreo de Movimiento del Mouse**: Captura las coordenadas del mouse en relación con un punto de origen.
* **Registro de Clics**: Registra las ubicaciones donde se realizan clics.
* **Interfaz Gráfica de Usuario (GUI)**: Controla el inicio y la detención del rastreo a través de una ventana de Tkinter intuitiva.
* **Visualización de Trayectoria**: Genera un gráfico de la trayectoria del mouse y los puntos de clic utilizando `matplotlib`.
* **Guardado Automático**: Guarda el gráfico de la trayectoria como una imagen PNG y los datos brutos como un archivo CSV al finalizar el rastreo.
* **Retraso de Inicio**: Incorpora un retraso de 5 segundos antes de comenzar el rastreo para dar tiempo al usuario a posicionar el mouse.

---

## Detalles del Código
tracking: Variable booleana global que controla si el rastreo está activo.
mouse_listener: Objeto pynput.mouse.Listener para capturar eventos del mouse.
activity_name: Nombre de la actividad ingresado por el usuario.
origin: Tupla (x, y) que almacena la posición del mouse cuando comienza el rastreo, sirviendo como punto de referencia (0,0) para las coordenadas relativas.
log_data: Lista de listas que almacena [actividad, tiempo, dx, dy] para cada movimiento del mouse.
clicks: Lista de tuplas (dx, dy) que almacena las posiciones relativas de los clics.
start_time, end_time: Registran el tiempo de inicio y fin del rastreo para calcular la duración.
plot_trajectory_and_save(): Función que utiliza matplotlib para generar y guardar el gráfico de la trayectoria y los clics.
save_csv(): Función para guardar los datos de log_data en un archivo CSV.
on_move(x, y): Callback para el evento de movimiento del mouse, registrando las coordenadas relativas.
on_click(x, y, button, pressed): Callback para el evento de clic del mouse, registrando las coordenadas relativas del clic.
delayed_start(): Inicia el mouse_listener después de un retraso de 5 segundos en un hilo separado.
start_tracking(): Manejador del botón "Iniciar Rastreo".
stop_tracking(): Manejador del botón "Detener Rastreo".
Interfaz Tkinter: Configura la ventana principal, los widgets de entrada, los botones y la etiqueta de estado.

## Notas Adicionales
Las coordenadas dx y dy son relativas al punto donde el mouse se encontraba después del retraso de 5 segundos al iniciar el rastreo.
La carpeta Trajectories se creará

Ejemplo:
![Stellar_Blade_20250611_233537_1689s](https://github.com/user-attachments/assets/d971a528-89e0-4022-bf4e-9e7b6d5205b3)
