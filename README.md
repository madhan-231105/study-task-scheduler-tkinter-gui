# Study Task Scheduler 📚⏳

A Python-based Task Management System built with **Tkinter**, **MySQL**, and **tkcalendar**.  
This application helps students schedule tasks, prioritize deadlines, track subjects, and visualize tasks using algorithms like **Heap Scheduling**, **Topological Sort**, and **Dynamic Programming**.

---

## 🚀 Features

### ✅ Task Management
- Add new tasks with:
  - Task Name  
  - Due Date  
  - Subject  
  - Status  
  - Cost (in hours)
- Edit task status
- Delete tasks
- View tasks in a clean table format (TreeView)

### 🧠 Algorithms Implemented
- **Heap Priority Scheduling**
  - Sorts tasks by calculated priority (High → Medium → Low)
- **Topological Sorting**
  - Orders tasks based on subject dependencies
- **Multistage Dynamic Programming**
  - Computes the optimal path based on minimum cost (time)

### 🎨 UI Features
- Modern Tkinter-based GUI  
- Color-coded buttons  
- Calendar date picker  
- Auto-priority calculation based on due date  

---

## 🛠️ Tech Stack

- **Python 3**
- **Tkinter**
- **MySQL + mysql-connector-python**
- **tkcalendar**
- **Heapq**, **Dynamic Programming**, **DFS**

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/study-task-scheduler.git
cd study-task-scheduler
