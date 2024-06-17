import tkinter as tk
from tkinter import filedialog, messagebox
import os
from functions import solomon_marcus, vasile_vasile, mihai_dinu

input_file_path = None

def open_file():
    global input_file_path
    input_file_path = filedialog.askopenfilename()
    if input_file_path:
        input_text.delete(1.0, tk.END)
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_text.insert(tk.END, file.read())

def remove_file():
    global input_file_path
    input_file_path = None
    input_text.delete(1.0, tk.END)
    messagebox.showinfo("Info", "Input file removed")

def save_to_output_file(content, method_name):
    if input_file_path:
        base_name = os.path.basename(input_file_path)
        name, ext = os.path.splitext(base_name)
        output_file_name = f"{name}_{method_name}_out.txt"

    with open(output_file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    messagebox.showinfo("Success", f"Output saved to {output_file_name}")

def process_text_or_file(process_function, method_name):
    global input_file_path
    choice = choice_var.get()
    input_str = input_text.get(1.0, tk.END).strip()
    if input_file_path:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_str = file.read().strip()
            output_str = process_function(input_str, choice)
            save_to_output_file(output_str, method_name)
            output_text.config(state=tk.NORMAL)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, output_str)
            output_text.config(state=tk.DISABLED)
    else:
        if not input_str:
            messagebox.showwarning("Warning", "No input text provided")
            return
        output_str = process_function(input_str, choice)
        output_text.config(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, output_str)
        output_text.config(state=tk.DISABLED)

window = tk.Tk()
window.title("Rhythm Analyzer")

# Frame pentru input și output
text_frame = tk.Frame(window)
text_frame.pack(fill=tk.BOTH, expand=True)

# Frame pentru input
input_frame = tk.Frame(text_frame)
input_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

input_label = tk.Label(input_frame, text="Input")
input_label.pack()

input_text = tk.Text(input_frame)
input_text.pack(fill=tk.BOTH, expand=True)

# Frame pentru output
output_frame = tk.Frame(text_frame)
output_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

output_label = tk.Label(output_frame, text="Output")
output_label.pack()

output_text = tk.Text(output_frame)
output_text.pack(fill=tk.BOTH, expand=True)
output_text.config(state=tk.DISABLED)

# Frame pentru butoane
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

remove_button = tk.Button(button_frame, text="Remove Input File", command=remove_file)
remove_button.pack(side=tk.LEFT)

file_button = tk.Button(button_frame, text="Load Input File", command=open_file)
file_button.pack(side=tk.LEFT)

choice_var = tk.StringVar(window)
choice_var.set("vers")  # Setarea opțiunii implicite

choice_menu = tk.OptionMenu(button_frame, choice_var, "vers", "frază")
choice_menu.pack(side=tk.LEFT)

solomon_button = tk.Button(button_frame, text="Solomon Marcus", command=lambda: process_text_or_file(solomon_marcus, "sm"))
solomon_button.pack(side=tk.LEFT)

mihai_button = tk.Button(button_frame, text="Mihai Dinu", command=lambda: process_text_or_file(mihai_dinu, "md"))
mihai_button.pack(side=tk.LEFT)

vasile_button = tk.Button(button_frame, text="Vasile Vasile", command=lambda: process_text_or_file(vasile_vasile, "vv"))
vasile_button.pack(side=tk.LEFT)

window.mainloop()
