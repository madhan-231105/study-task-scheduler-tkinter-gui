import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import date, datetime
import mysql.connector
import heapq

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="madhan123",
    database="study"
)
cursor = conn.cursor()

# Helper Functions
def calculate_priority(due_date):
    today = date.today()
    delta = (due_date - today).days
    if delta <= 2:
        return "High"
    elif 3 <= delta <= 5:
        return "Medium"
    else:
        return "Low"

# Main Window
def open_task_scheduler():
    scheduler = tk.Tk()
    scheduler.title("Task Management System")
    scheduler.geometry("1100x600")
    scheduler.configure(bg="#2C3E50")

    frame = tk.Frame(scheduler, bg="#2C3E50")
    frame.pack(pady=10)

    labels = ["Task Name", "Due Date", "Subject", "Status", "Cost"]
    entries = {}

    for i, text in enumerate(labels):
        label = tk.Label(frame, text=text, fg="white", bg="#2C3E50", font=("Arial", 12))
        label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        if text == "Due Date":
            entry = DateEntry(frame, font=("Arial", 12), date_pattern='yyyy-mm-dd', mindate=date.today())
        elif text == "Status":
            entry = ttk.Combobox(frame, values=["Pending", "In Progress", "Completed"], font=("Arial", 12), state="readonly")
            entry.set("Pending")
        else:
            entry = tk.Entry(frame, font=("Arial", 12))
        entry.grid(row=i, column=1, pady=5)
        entries[text] = entry

    def load_tasks():
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", "end", values=row)

    def add_task():
        task = entries["Task Name"].get()
        due = entries["Due Date"].get_date()
        subj = entries["Subject"].get()
        stat = entries["Status"].get()
        cost = entries["Cost"].get()
        prio = calculate_priority(due)

        if not (task and subj and stat and cost):
            messagebox.showerror("Error", "Fill all fields")
            return

        cursor.execute("INSERT INTO tasks (task_name, priority, due_date, subject, status, cost) VALUES (%s, %s, %s, %s, %s, %s)",
                       (task, prio, due, subj, stat, int(cost)))
        conn.commit()
        load_tasks()
        messagebox.showinfo("Success", "Task Added")

    def delete_task():
        sel = tree.selection()
        if sel:
            task_id = tree.item(sel, 'values')[0]
            cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
            conn.commit()
            load_tasks()

    def update_status():
        sel = tree.selection()
        if sel:
            task_id = tree.item(sel, 'values')[0]
            new_stat = status_cb.get()
            cursor.execute("UPDATE tasks SET status=%s WHERE id=%s", (new_stat, task_id))
            conn.commit()
            load_tasks()

    def heap_priority_schedule():
        cursor.execute("SELECT * FROM tasks WHERE status != 'Completed'")
        rows = cursor.fetchall()
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        heap = [(priority_map[row[2]], row) for row in rows]
        heapq.heapify(heap)
        tree.delete(*tree.get_children())
        while heap:
            task = heapq.heappop(heap)[1]
            tree.insert("", "end", values=task)

    def topological_sort():
        cursor.execute("SELECT subject FROM tasks GROUP BY subject")
        subjects = [row[0] for row in cursor.fetchall()]
        graph = {subj: [] for subj in subjects}

        cursor.execute("SELECT * FROM tasks")
        all_tasks = cursor.fetchall()
        for task in all_tasks:
            for dep in subjects:
                if dep != task[4]:
                    graph[dep].append(task[4])

        visited, stack = set(), []

        def dfs(v):
            visited.add(v)
            for nei in graph.get(v, []):
                if nei not in visited:
                    dfs(nei)
            stack.append(v)

        for s in subjects:
            if s not in visited:
                dfs(s)

        sorted_tasks = []
        while stack:
            subj = stack.pop()
            cursor.execute("SELECT * FROM tasks WHERE subject=%s", (subj,))
            sorted_tasks.extend(cursor.fetchall())

        tree.delete(*tree.get_children())
        for t in sorted_tasks:
            tree.insert("", "end", values=t)

    def multistage_dp():
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        stages = {}
        for task in tasks:
            stages.setdefault(task[4], []).append(task)

        path, cost = [], 0
        for subj in stages:
            best = min(stages[subj], key=lambda x: x[6])
            path.append(best)
            cost += best[6]

        tree.delete(*tree.get_children())
        for task in path:
            tree.insert("", "end", values=task)
        messagebox.showinfo("DP Result", f"Optimal Path Cost(time): {cost}")

    add_btn = tk.Button(frame, text="Add Task", command=add_task, bg="#1ABC9C", fg="white", font=("Arial", 12, "bold"))
    add_btn.grid(row=len(labels), columnspan=2, pady=10)

    tree = ttk.Treeview(scheduler, columns=("ID", "Name", "Priority", "Due", "Subject", "Status", "Cost(hours)"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(pady=20, fill="both", expand=True)

    status_cb = ttk.Combobox(scheduler, values=["Pending", "In Progress", "Completed"], font=("Arial", 12), state="readonly")
    status_cb.set("Pending")
    status_cb.pack(pady=5)

    update_btn = tk.Button(scheduler, text="Update Status", command=update_status, bg="#2980B9", fg="white")
    update_btn.pack(pady=5)

    del_btn = tk.Button(scheduler, text="Delete Task", command=delete_task, bg="#E74C3C", fg="white")
    del_btn.pack(pady=5)

    heap_btn = tk.Button(scheduler, text="Heap Scheduling", command=heap_priority_schedule, bg="#F39C12", fg="white")
    heap_btn.pack(pady=5)

    topo_btn = tk.Button(scheduler, text="Topological Sort", command=topological_sort, bg="#8E44AD", fg="white")
    topo_btn.pack(pady=5)

    dp_btn = tk.Button(scheduler, text="DP Optimal Path", command=multistage_dp, bg="#16A085", fg="white")
    dp_btn.pack(pady=5)

    load_tasks()
    scheduler.mainloop()

open_task_scheduler()
