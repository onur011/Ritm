import tkinter as tk
from tkinter import filedialog, messagebox
from functions import solomon_marcus, vasile_vasile

input_file_path = None

def open_file():
    global input_file_path
    input_file_path = filedialog.askopenfilename()
    if input_file_path:

        input_text.delete(1.0, tk.END)

def save_to_output_file(content):
    with open("output.txt", 'w', encoding='utf-8') as file:
        file.write(content)
    messagebox.showinfo("Success", "Output saved to output.txt")

def process_text_or_file(process_function):
    global input_file_path
    input_str = input_text.get(1.0, tk.END).strip()
    if input_file_path:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_str = file.read().strip()
            output_str = process_function(input_str)
            save_to_output_file(output_str)
    else:
        if not input_str:
            messagebox.showwarning("Warning", "No input text provided")
            return
        output_str = process_function(input_str)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, output_str)

window = tk.Tk()
window.title("Text Processor")

input_label = tk.Label(window, text="Input")
input_label.pack()

input_text = tk.Text(window, height=20, width=100)
input_text.pack()

output_label = tk.Label(window, text="Output")
output_label.pack()


output_text = tk.Text(window, height=20, width=100)
output_text.pack()


file_button = tk.Button(window, text="Load Input File", command=open_file)
file_button.pack()

solomon_button = tk.Button(window, text="Solomon Marcus", command=lambda: process_text_or_file(solomon_marcus))
solomon_button.pack()

vasile_button = tk.Button(window, text="Vasile Vasile", command=lambda: process_text_or_file(vasile_vasile))
vasile_button.pack()


window.mainloop()
