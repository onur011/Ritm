import tkinter as tk
from tkinter import filedialog, messagebox
from functions import solomon_marcus, vasile_vasile, mihai_dinu

input_file_path = None

def open_file():
    global input_file_path
    input_file_path = filedialog.askopenfilename()
    if input_file_path:
        input_text.delete(1.0, tk.END)
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_text.insert(tk.END, file.read())

def save_to_output_file(content):
    with open("output.txt", 'w', encoding='utf-8') as file:
        file.write(content)
    messagebox.showinfo("Success", "Output saved to output.txt")

def process_text_or_file(process_function):
    global input_file_path
    choice = choice_var.get()
    input_str = input_text.get(1.0, tk.END).strip()
    if input_file_path:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_str = file.read().strip()
            output_str = process_function(input_str,choice)
            save_to_output_file(output_str)
    else:
        if not input_str:
            messagebox.showwarning("Warning", "No input text provided")
            return
        output_str = process_function(input_str,choice)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, output_str)

window = tk.Tk()
window.title("Rhythm Analyzer")

input_label = tk.Label(window, text="Input")
input_label.pack()

input_text = tk.Text(window, height=10, width=80)
input_text.pack()

output_label = tk.Label(window, text="Output")
output_label.pack()

output_text = tk.Text(window, height=10, width=80)
output_text.pack()

# Frame pentru butoane
button_frame = tk.Frame(window)
button_frame.pack()

file_button = tk.Button(button_frame, text="Load Input File", command=open_file)
file_button.pack(side=tk.LEFT)

choice_var = tk.StringVar(window)
choice_var.set("vers")  # Setarea opțiunii implicite

choice_menu = tk.OptionMenu(button_frame, choice_var, "vers", "frază")
choice_menu.pack(side=tk.LEFT)

solomon_button = tk.Button(button_frame, text="Solomon Marcus", command=lambda: process_text_or_file(solomon_marcus))
solomon_button.pack(side=tk.LEFT)

mihai_button = tk.Button(button_frame, text="Mihai Dinu", command=lambda: process_text_or_file(mihai_dinu))
mihai_button.pack(side=tk.LEFT)

vasile_button = tk.Button(button_frame, text="Vasile Vasile", command=lambda: process_text_or_file(vasile_vasile))
vasile_button.pack(side=tk.LEFT)

window.mainloop()
