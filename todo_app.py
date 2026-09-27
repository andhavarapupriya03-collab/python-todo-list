import tkinter as tk
from tkinter import messagebox
import sqlite3


# ---------------- DATABASE ----------------

conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

conn.commit()


# ---------------- FUNCTIONS ----------------

def load_tasks():
    task_list.delete(0, tk.END)

    cursor.execute("SELECT id, task, status FROM tasks")
    tasks = cursor.fetchall()

    for task_id, task, status in tasks:
        task_list.insert(
            tk.END,
            f"{task_id}. {task} - {status}"
        )


def add_task():
    task = task_entry.get()

    if task.strip() == "":
        messagebox.showwarning("Warning", "Please enter a task.")
        return

    cursor.execute(
        "INSERT INTO tasks (task, status) VALUES (?, ?)",
        (task, "Pending")
    )

    conn.commit()

    task_entry.delete(0, tk.END)
    load_tasks()


def complete_task():
    selected = task_list.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a task."
        )
        return

    task_text = task_list.get(selected[0])

    task_id = task_text.split(".")[0]

    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        ("Completed", task_id)
    )

    conn.commit()

    load_tasks()


def delete_task():
    selected = task_list.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a task."
        )
        return

    task_text = task_list.get(selected[0])

    task_id = task_text.split(".")[0]

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()

    load_tasks()


# ---------------- GUI ----------------

root = tk.Tk()

root.title("To-Do List Application")
root.geometry("500x500")

title = tk.Label(
    root,
    text="My To-Do List",
    font=("Arial", 22, "bold")
)

title.pack(pady=20)


task_entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 14)
)

task_entry.pack(pady=10)


add_button = tk.Button(
    root,
    text="Add Task",
    width=15,
    command=add_task
)

add_button.pack(pady=5)


task_list = tk.Listbox(
    root,
    width=50,
    height=12,
    font=("Arial", 12)
)

task_list.pack(pady=15)


complete_button = tk.Button(
    root,
    text="Mark Completed",
    width=15,
    command=complete_task
)

complete_button.pack(pady=5)


delete_button = tk.Button(
    root,
    text="Delete Task",
    width=15,
    command=delete_task
)

delete_button.pack(pady=5)


load_tasks()

root.mainloop()