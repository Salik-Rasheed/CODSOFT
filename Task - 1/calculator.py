import tkinter as tk
import re
import math

# ---------------- DATA ----------------
history = []
history_visible = False
sci_visible = False
memory = 0

# ---------------- EVALUATION ----------------
def evaluate_expression(expr):
    try:
        if expr.strip() == "":
            return ""

        expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**")

        expr = expr.replace("π", str(math.pi))
        expr = expr.replace("e", str(math.e))

        expr = expr.replace("√(", "math.sqrt(")
        expr = expr.replace("log(", "math.log10(")
        expr = expr.replace("ln(", "math.log(")

        expr = re.sub(r'(\d+)!', r'math.factorial(\1)', expr)

        while expr and expr[-1] in "+-*/.":
            expr = expr[:-1]

        expr = re.sub(r'(\d+\.?\d*)%', r'(\1/100)', expr)

        return round(eval(expr, {"math": math}), 6)

    except:
        return "Error"

# ---------------- CLICK ----------------
def click(value):
    global memory
    current = entry_var.get()

    if value == "=":
        result = evaluate_expression(current)
        entry_var.set(result)

        if result != "Error":
            record = f"{current} = {result}"
            history.append(record)
            history_list.insert(tk.END, record)

    elif value == "AC":
        entry_var.set("")

    elif value == "⌫":
        entry_var.set(current[:-1])

    elif value == "+/-":
        if current:
            if current.startswith("-"):
                entry_var.set(current[1:])
            else:
                entry_var.set("-" + current)

    elif value == "MC":
        memory = 0

    elif value == "MR":
        entry.insert(tk.END, str(memory))

    elif value == "M+":
        try:
            memory += float(evaluate_expression(current))
        except:
            pass

    elif value == "M-":
        try:
            memory -= float(evaluate_expression(current))
        except:
            pass

    elif value == "SCI":
        toggle_sci()

    else:
        entry.insert(tk.END, value)

# ---------------- SCI CLICK ----------------
def sci_click(val):
    if val == "x²":
        entry.insert(tk.END, "^2")
    elif val == "x³":
        entry.insert(tk.END, "^3")
    elif val == "1/x":
        entry.insert(tk.END, "1/(")
    else:
        entry.insert(tk.END, val)

# ---------------- SCI TOGGLE ----------------
def toggle_sci():
    global sci_visible
    if sci_visible:
        sci_frame.pack_forget()
        sci_visible = False
    else:
        sci_frame.pack(fill="x")
        sci_visible = True

# ---------------- HISTORY ----------------
def use_history(event):
    selected = history_list.curselection()
    if selected:
        text = history_list.get(selected[0])
        entry_var.set(text.split("=")[0].strip())

# ---------------- SLIDE ----------------
def toggle_history():
    global history_visible

    if history_visible:
        arrow_btn.config(text="⬇")
        show_main_ui()
        slide_up()
        history_visible = False
    else:
        arrow_btn.config(text="⬆")
        hide_main_ui()
        slide_down()
        history_visible = True

def slide_down(h=0):
    if h <= 300:
        history_frame.place(height=h)
        root.after(5, lambda: slide_down(h + 15))

def slide_up(h=300):
    if h >= 0:
        history_frame.place(height=h)
        root.after(5, lambda: slide_up(h - 15))

# ---------------- SHOW/HIDE ----------------
def hide_main_ui():
    entry.pack_forget()
    frame.pack_forget()
    sci_frame.pack_forget()

def show_main_ui():
    entry.pack(fill=tk.BOTH, padx=10, pady=10)
    frame.pack(expand=True, fill="both")
    if sci_visible:
        sci_frame.pack(fill="x")

# ---------------- KEYBOARD ----------------
def key_press(event):
    key = event.char
    if key in "0123456789+-*/.%()":
        entry.insert(tk.END, key)
    elif event.keysym == "Return":
        click("=")
    elif event.keysym == "BackSpace":
        entry_var.set(entry_var.get()[:-1])

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Calculator")
root.geometry("300x580")
root.configure(bg="#010101")

entry_var = tk.StringVar()

# Arrow
arrow_btn = tk.Button(root, text="⬇", font=("Arial", 14),
                      command=toggle_history,
                      bg="#3c3f41", fg="white")
arrow_btn.place(relx=0.5, y=5, anchor="n")

# History
history_frame = tk.Frame(root, bg="#1e1e1e")
history_frame.place(relx=0.5, y=30, anchor="n", width=280, height=0)

history_list = tk.Listbox(history_frame, bg="#2d2d2d", fg="white")
history_list.pack(expand=True, fill="both", padx=10, pady=10)
history_list.bind("<<ListboxSelect>>", use_history)

# Display
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 22),
                 bd=10, relief=tk.FLAT, justify="right",
                 bg="#2d2d2d", fg="white", insertbackground="white")
entry.pack(fill=tk.BOTH, padx=10, pady=10)

# Buttons Layout
frame = tk.Frame(root, bg="#000000")
frame.pack(expand=True, fill="both")

buttons = [
    ("MC", "MR", "M+", "M-"),
    ("AC", "+/-", "%", "/"),
    ("7", "8", "9", "*"),
    ("4", "5", "6", "-"),
    ("1", "2", "3", "+"),
    ("0", ".", "=", "SCI")
]

for r, row in enumerate(buttons):
    for c, val in enumerate(row):
        tk.Button(frame, text=val, font=("Arial", 14),
                  command=lambda v=val: click(v),
                  bg="#000000", fg="white"
                  ).grid(row=r, column=c, sticky="nsew", ipadx=10, ipady=15)

# Grid Config
for i in range(len(buttons)):
    frame.grid_rowconfigure(i, weight=1)
for i in range(4):
    frame.grid_columnconfigure(i, weight=1)

# SCI FRAME
sci_frame = tk.Frame(root, bg="#000000")

sci_buttons = [
    ["√(", "^", "log(", "ln("],
    ["x²", "x³", "1/x", "!"],
    ["π", "e",")"]
]

for r, row in enumerate(sci_buttons):
    for c, val in enumerate(row):
        tk.Button(sci_frame, text=val, font=("Arial", 12),
                  command=lambda v=val: sci_click(v),
                  bg="#000000", fg="white"
                  ).grid(row=r, column=c, sticky="nsew", ipadx=5, ipady=10)

for i in range(4):
    sci_frame.grid_columnconfigure(i, weight=1)

# Keyboard
root.bind("<Key>", key_press)

root.mainloop()
