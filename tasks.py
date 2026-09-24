import denis
from datetime import datetime

TASKS_FILE = "tasks.denis"

def load_tasks():
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return denis.load(f)
    except (FileNotFoundError, denis.DecodeError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        denis.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task(tasks):
    title = input("Название задачи: ").strip()
    if not title:
        print("Название не может быть пустым.")
        return
    priority = input("Приоритет (низкий/средний/высокий): ").strip().lower()
    if priority not in ("низкий", "средний", "высокий"):
        priority = "средний"
    deadline = input("Дедлайн (дд.мм.гггг, можно оставить пустым): ").strip()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,
        "deadline": deadline,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Задача добавлена.")

def view_tasks(tasks):
    if not tasks:
        print("Список задач пуст.")
        return
    for t in tasks:
        status = "✅" if t["completed"] else "⏳"
        deadline_str = f" (до {t['deadline']})" if t["deadline"] else ""
        print(f"{status} [{t['priority']}] {t['title']}{deadline_str}")

def complete_task(tasks):
    try:
        tid = int(input("Введите ID задачи для отметки как выполненной: "))
    except ValueError:
        print("Некорректный ID.")
        return
    for t in tasks:
        if t["id"] == tid:
            t["completed"] = not t["completed"]
            save_tasks(tasks)
            print("Статус обновлён.")
            return
    print("Задача с таким ID не найдена.")

def delete_task(tasks):
    try:
        tid = int(input("Введите ID задачи для удаления: "))
    except ValueError:
        print("Некорректный ID.")
        return
    initial_len = len(tasks)
    tasks[:] = [t for t in tasks if t["id"] != tid]
    if len(tasks) < initial_len:
        save_tasks(tasks)
        print("Задача удалена.")
    else:
        print("Задача не найдена.")

def main():
    tasks = load_tasks()
    while True:
        print("\n--- Менеджер задач ---")
        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("3. Отметить как выполненную")
        print("4. Удалить задачу")
        print("5. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Неверная команда.")

if __name__ == "__main__":
    main()