import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog  # Importa simpledialog
import serial
import threading
import time
from PIL import Image, ImageDraw, ImageTk

# Configuración inicial de colores
PRIMARY_COLOR = "#5126f0"
SECONDARY_COLOR = "#8226f0"
ACCENT_COLOR = "#21b8ff"
BACKGROUND_LIGHT = "#fff"
BACKGROUND_DARK = "#000"
TEXT_COLOR_LIGHT = "#000"
TEXT_COLOR_DARK = "#fff"

class TemperatureTherapyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz Terapia Neonatal")
        self.serial_connection = None
        self.running = False
        self.temperature = 0.0
        self.remaining_time = 0

        # Variable para modo noche
        self.dark_mode = tk.BooleanVar(value=False)

        # Configuración de la interfaz principal
        self.root.geometry("500x600")
        self.root.configure(bg=BACKGROUND_LIGHT)

        # Encabezado
        self.header = tk.Frame(self.root, bg=PRIMARY_COLOR)
        self.header.pack(fill=tk.X)

        self.title_label = tk.Label(
            self.header, text="Interfaz Terapia Neonatal", font=("Helvetica", 16), bg=PRIMARY_COLOR, fg=TEXT_COLOR_DARK
        )
        self.title_label.pack(pady=10)

        # Sección de temperatura
        self.temp_canvas = tk.Canvas(self.root, width=400, height=400, bg=BACKGROUND_LIGHT, highlightthickness=0)
        self.temp_canvas.pack(pady=20)

        # Etiqueta de tiempo restante
        self.timer_label = tk.Label(self.root, text="Time: 00:00", font=("Helvetica", 14), bg=BACKGROUND_LIGHT, fg=TEXT_COLOR_LIGHT)
        self.timer_label.pack(pady=10)

        # Botones
        self.control_frame = tk.Frame(self.root, bg=BACKGROUND_LIGHT)
        self.control_frame.pack(pady=10)

        self.start_button = ttk.Button(self.control_frame, text="Iniciar Terapia", command=self.start_therapy)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(self.control_frame, text="Terminar Terapia", command=self.stop_therapy)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.mode_button = ttk.Checkbutton(
            self.control_frame, text="Night Mode", variable=self.dark_mode, command=self.toggle_mode
        )
        self.mode_button.grid(row=0, column=2, padx=5)

        # Configuración inicial del canvas
        self.draw_temperature(0.0, "Low")

    def toggle_mode(self):
        if self.dark_mode.get():
            self.root.configure(bg=BACKGROUND_DARK)
            self.temp_canvas.configure(bg=BACKGROUND_DARK)
            self.timer_label.configure(bg=BACKGROUND_DARK, fg=TEXT_COLOR_LIGHT)
        else:
            self.root.configure(bg=BACKGROUND_LIGHT)
            self.temp_canvas.configure(bg=BACKGROUND_LIGHT)
            self.timer_label.configure(bg=BACKGROUND_LIGHT, fg=TEXT_COLOR_LIGHT)

    # def draw_temperature(self, temperature, status):
    #     """Dibuja el dial de temperatura en el canvas"""
    #     self.temp_canvas.delete("all")

    #     # Crear imagen con degradado dinámico
    #     image = Image.new("RGBA", (400, 400), BACKGROUND_LIGHT if not self.dark_mode.get() else BACKGROUND_DARK)
    #     draw = ImageDraw.Draw(image)

    #     # Dibujar arco
    #     start_angle = -90
    #     end_angle = (temperature / 40.0) * 360 - 90
    #     color = self.get_temperature_color(temperature)

    #     draw.pieslice([50, 50, 350, 350], start_angle, end_angle, fill=color, outline=color)

    #     # Dibujar círculo negro detrás del texto
    #     draw.ellipse([150, 150, 250, 250], fill="#000000")

    #     # Convertir imagen a objeto compatible con Tkinter
    #     self.tk_image = ImageTk.PhotoImage(image)
    #     self.temp_canvas.create_image(200, 200, image=self.tk_image)

    #     # Texto de temperatura
    #     self.temp_canvas.create_text(
    #         200, 200, text=f"{temperature:.1f}°C", font=("Helvetica", 24), fill=TEXT_COLOR_LIGHT if self.dark_mode.get() else TEXT_COLOR_DARK
    #     )

    def draw_temperature(self, temperature, status):
        """Dibuja el dial de temperatura en el canvas"""
        self.temp_canvas.delete("all")

        # Crear imagen con degradado dinámico
        image = Image.new("RGBA", (400, 400), BACKGROUND_LIGHT if not self.dark_mode.get() else BACKGROUND_DARK)
        draw = ImageDraw.Draw(image)

        # Dibujar arco
        start_angle = -90
        end_angle = (temperature / 40.0) * 360 - 90
        color = self.get_temperature_color(temperature)

        draw.pieslice([50, 50, 350, 350], start_angle, end_angle, fill=color, outline=color)

        # Cambiar el color del círculo detrás del texto según el modo
        circle_fill = BACKGROUND_LIGHT if self.dark_mode.get() else BACKGROUND_DARK
        draw.ellipse([150, 150, 250, 250], fill=circle_fill)

        # Convertir imagen a objeto compatible con Tkinter
        self.tk_image = ImageTk.PhotoImage(image)
        self.temp_canvas.create_image(200, 200, image=self.tk_image)

        # Texto de temperatura
        self.temp_canvas.create_text(
            200, 200, text=f"{temperature:.1f}°C", font=("Helvetica", 24), fill=TEXT_COLOR_LIGHT if self.dark_mode.get() else TEXT_COLOR_DARK
        )


    def get_temperature_color(self, temperature):
        """Determina el color del arco basado en la temperatura"""
        if temperature <= 30:
            return "#0000ff"  # Azul para temperaturas bajas
        elif 30 < temperature < 38:
            return "#ffa500"  # Naranja para temperaturas medias
        else:
            return "#ff0000"  # Rojo para temperaturas altas

    def start_therapy(self):
        """Inicia la terapia y la lectura del puerto COM"""
        port = tk.simpledialog.askstring("Port", "Enter the COM port (e.g., COM3):")
        self.remaining_time = tk.simpledialog.askinteger("Time", "Enter therapy time (minutes):") * 60

        if not port or not self.remaining_time:
            messagebox.showerror("Error", "Please provide valid port and time!")
            return

        try:
            self.serial_connection = serial.Serial(port, 9600, timeout=1)
            self.running = True
            threading.Thread(target=self.read_serial_data, daemon=True).start()
            self.update_timer()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open serial port: {e}")

    def stop_therapy(self):
        """Detiene la terapia"""
        self.running = False
        if self.serial_connection:
            self.serial_connection.close()
        self.timer_label.config(text="Time: 00:00")

    def read_serial_data(self):
        """Lee los datos del puerto serie y actualiza la temperatura"""
        while self.running:
            try:
                line = self.serial_connection.readline().decode("utf-8").strip()
                if line.endswith("C"):
                    self.temperature = float(line[:-1])
                    status = "Low" if self.temperature <= 15 else "Medium" if self.temperature < 20 else "High"
                    self.draw_temperature(self.temperature, status)
            except Exception as e:
                print(f"Error reading serial data: {e}")

    def update_timer(self):
        """Actualiza el cronómetro de cuenta regresiva"""
        if self.running and self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"Time: {mins:02}:{secs:02}")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.stop_therapy()
            self.play_alarm()

    def play_alarm(self):
        """Reproduce una alarma sonora"""
        for _ in range(3):
            print("Alarm sound!")  # Aquí puedes usar winsound o cualquier librería para emitir sonidos
            time.sleep(0.5)

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureTherapyApp(root)
    root.mainloop()
