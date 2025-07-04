import tkinter as tk
from tkinter import scrolledtext

class MainWindow:
    def __init__(self, agent):
        self.agent = agent
        self.window = tk.Tk()
        self.window.title("Jaime - Agente IA")

        self.input_label = tk.Label(self.window, text="Introduce tu comando:")
        self.input_label.pack()

        self.input_text = tk.Entry(self.window, width=50)
        self.input_text.pack()

        self.run_button = tk.Button(self.window, text="Ejecutar", command=self.run_command)
        self.run_button.pack()

        self.output_text = scrolledtext.ScrolledText(self.window, width=60, height=20)
        self.output_text.pack()

    def run_command(self):
        input_text = self.input_text.get()
        response = self.agent.run(input_text)
        self.output_text.insert(tk.END, f"Entrada: {input_text}\nSalida: {response}\n\n")
        self.input_text.delete(0, tk.END)

    def run(self):
        self.window.mainloop()