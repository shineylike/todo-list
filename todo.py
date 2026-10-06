"""Logică pentru gestionarea sarcinilor To-Do."""

import json
from pathlib import Path
from typing import Dict, List, Union


TASKS_FILE = Path(__file__).with_name("tasks.json")
Task = Dict[str, Union[int, str, bool]]
FilePath = Union[str, Path]


def _validate_task_id(task_id: int) -> None:
    if isinstance(task_id, bool) or not isinstance(task_id, int) or task_id < 1:
        raise ValueError("ID-ul sarcinii trebuie să fie un număr întreg pozitiv.")


def _validate_tasks(tasks: object) -> List[Task]:
    if not isinstance(tasks, list):
        raise ValueError("Fișierul de sarcini trebuie să conțină o listă.")

    validated: List[Task] = []
    seen_ids = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("Fiecare sarcină trebuie să fie un obiect.")

        task_id = task.get("id")
        title = task.get("title")
        completed = task.get("completed")
        _validate_task_id(task_id)
        if task_id in seen_ids:
            raise ValueError("ID-urile sarcinilor trebuie să fie unice.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Titlul sarcinii nu poate fi gol.")
        if not isinstance(completed, bool):
            raise ValueError("Starea sarcinii trebuie să fie adevărată sau falsă.")

        seen_ids.add(task_id)
        validated.append(
            {"id": task_id, "title": title.strip(), "completed": completed}
        )
    return validated


def load_tasks(file_path: FilePath = TASKS_FILE) -> List[Task]:
    """Încarcă sarcinile; un fișier absent sau gol reprezintă o listă goală."""
    path = Path(file_path)
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as tasks_file:
        contents = tasks_file.read()
    if not contents.strip():
        return []
    return _validate_tasks(json.loads(contents))


def save_tasks(tasks: List[Task], file_path: FilePath = TASKS_FILE) -> None:
    """Validează și salvează sarcinile în format JSON."""
    validated_tasks = _validate_tasks(tasks)
    path = Path(file_path)
    with path.open("w", encoding="utf-8") as tasks_file:
        json.dump(validated_tasks, tasks_file, ensure_ascii=False, indent=2)
        tasks_file.write("\n")


def add_task(title: str, file_path: FilePath = TASKS_FILE) -> Task:
    """Adaugă o sarcină cu titlu valid și întoarce sarcina creată."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Titlul sarcinii nu poate fi gol.")

    tasks = load_tasks(file_path)
    task = {
        "id": max((item["id"] for item in tasks), default=0) + 1,
        "title": title.strip(),
        "completed": False,
    }
    tasks.append(task)
    save_tasks(tasks, file_path)
    return task


def delete_task(task_id: int, file_path: FilePath = TASKS_FILE) -> None:
    """Șterge sarcina indicată; ridică LookupError dacă nu există."""
    _validate_task_id(task_id)
    tasks = load_tasks(file_path)
    remaining_tasks = [task for task in tasks if task["id"] != task_id]
    if len(remaining_tasks) == len(tasks):
        raise LookupError("Sarcina solicitată nu există.")
    save_tasks(remaining_tasks, file_path)


def mark_task_completed(task_id: int, file_path: FilePath = TASKS_FILE) -> Task:
    """Marchează sarcina ca finalizată și întoarce sarcina actualizată."""
    _validate_task_id(task_id)
    tasks = load_tasks(file_path)
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks, file_path)
            return task
    raise LookupError("Sarcina solicitată nu există.")


def toggle_task(task_id: int, file_path: FilePath = TASKS_FILE) -> Task:
    """Inversează starea sarcinii și întoarce sarcina actualizată."""
    _validate_task_id(task_id)
    tasks = load_tasks(file_path)
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            save_tasks(tasks, file_path)
            return task
    raise LookupError("Sarcina solicitată nu există.")
