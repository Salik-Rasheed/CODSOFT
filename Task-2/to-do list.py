import tkinter as tk
from tkinter import messagebox, ttk
import json
import datetime

# -------- FILE HANDLING --------
def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            return json.load(f)
    except:
        return []


def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)


class ModernTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 To-Do List")
        self.root.geometry("650x550")
        self.root.configure(bg="#1e1e2f")

        self.tasks = load_tasks()

        # -------- TITLE --------
        title = tk.Label(root, text="✨ To-Do List ✨", font=("Segoe UI", 18, "bold"), bg="#1e1e2f", fg="#ffffff")
        title.pack(pady=10)

        # -------- INPUT FRAME --------
        input_frame = tk.Frame(root, bg="#1e1e2f")
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(input_frame, width=35, font=("Segoe UI", 12))
        self.task_entry.grid(row=0, column=0, padx=5)

        self.priority = ttk.Combobox(input_frame, values=["High", "Medium", "Low"], width=10)
        self.priority.set("Medium")
        self.priority.grid(row=0, column=1, padx=5)

        add_btn = tk.Button(input_frame, text="➕ Add", command=self.add_task, bg="#4CAF50", fg="white", width=10)
        add_btn.grid(row=0, column=2, padx=5)

        # -------- LIST FRAME --------
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10)

        self.tree = ttk.Treeview(list_frame, columns=("Task", "Priority", "Status", "Time"), show="headings", height=15)
        self.tree.heading("Task", text="Task")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Time", text="Created")

        self.tree.column("Task", width=200)
        self.tree.column("Priority", width=80)
        self.tree.column("Status", width=80)
        self.tree.column("Time", width=150)

        self.tree.pack()

        # -------- BUTTONS --------
        btn_frame = tk.Frame(root, bg="#1e1e2f")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="✅ Mark Done", command=self.mark_done, bg="#2196F3", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="🗑 Delete", command=self.delete_task, bg="#f44336", fg="white", width=15).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="✏ Update", command=self.update_task, bg="#ff9800", fg="white", width=15).grid(row=0, column=2, padx=5)

        self.refresh()

    # -------- FUNCTIONS --------
    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter a task")
            return

        task = {
            "title": text,
            "priority": self.priority.get(),
            "done": False,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.tasks.append(task)
        save_tasks(self.tasks)
        self.task_entry.delete(0, tk.END)
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, task in enumerate(self.tasks):
            status = "Done" if task["done"] else "Pending"
            self.tree.insert("", "end", iid=i, values=(task["title"], task["priority"], status, task["time"]))

    def mark_done(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task")
            return

        index = int(selected[0])
        self.tasks[index]["done"] = True
        save_tasks(self.tasks)
        self.refresh()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task")
            return

        index = int(selected[0])
        self.tasks.pop(index)
        save_tasks(self.tasks)
        self.refresh()

    def update_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task")
            return

        index = int(selected[0])

        new_text = self.task_entry.get().strip()
        if not new_text:
            messagebox.showwarning("Warning", "Enter new task in box")
            return

        self.tasks[index]["title"] = new_text
        self.tasks[index]["priority"] = self.priority.get()
        save_tasks(self.tasks)
        self.refresh()


# -------- RUN --------
root = tk.Tk()
app = ModernTodoApp(root)
root.mainloop()
