import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

# Файл данных
DATA_FILE = 'data.json'

# Создаем главное окно
root = tk.Tk()
root.title("Training Planner")

# Функции для работы с данными
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Вводные поля
frame_form = ttk.Frame(root)
frame_form.pack(pady=10)

# Поля
ttk.Label(frame_form, text="Дата (дд-мм-гггг):").grid(row=0, column=0, padx=5)
entry_date = ttk.Entry(frame_form)
entry_date.grid(row=0, column=1, padx=5)

ttk.Label(frame_form, text="Тип тренировки:").grid(row=1, column=0, padx=5)
entry_type = ttk.Entry(frame_form)
entry_type.grid(row=1, column=1, padx=5)

ttk.Label(frame_form, text="Длительность (мин):").grid(row=2, column=0, padx=5)
entry_duration = ttk.Entry(frame_form)
entry_duration.grid(row=2, column=1, padx=5)

# Таблица
columns = ('date', 'type', 'duration')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.pack(pady=10)

# Функция добавления
def add_training():
    date_str = entry_date.get()
    t_type = entry_type.get()
    duration_str = entry_duration.get()

    # Валидация
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        messagebox.showerror("Ошибочка!", "Некорректный формат даты.")
        return
    if not duration_str.isdigit() or int(duration_str) <= 0:
        messagebox.showerror("Ошибочка!", "Длительность должна быть положительным числом.")
        return

    duration = int(duration_str)
    new_entry = {'date': date_str, 'type': t_type, 'duration': duration}

    # Добавляем в таблицу
    tree.insert('', 'end', values=(date_str, t_type, duration))
    # Загружаем текущие данные и сохраняем
    data = load_data()
    data.append(new_entry)
    save_data(data)

# Кнопка добавить
btn_add = ttk.Button(root, text="Добавить тренировку", command=add_training)
btn_add.pack(pady=5)

# Загружаем данные при запуске
for item in load_data():
    tree.insert('', 'end', values=(item['date'], item['type'], item['duration']))

# Запуск GUI
root.mainloop()