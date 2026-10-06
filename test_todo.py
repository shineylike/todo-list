"""Teste pentru logica de gestionare a sarcinilor."""

import pytest

from todo import (
    add_task,
    delete_task,
    load_tasks,
    mark_task_completed,
    toggle_task,
)


def test_add_task_saves_valid_task(tmp_path):
    tasks_file = tmp_path / "tasks.json"

    task = add_task("Cumpărături", tasks_file)

    assert task == {"id": 1, "title": "Cumpărături", "completed": False}
    assert load_tasks(tasks_file) == [task]


@pytest.mark.parametrize("title", ["", " ", "   ", "\t\n"])
def test_add_task_rejects_empty_title(tmp_path, title):
    tasks_file = tmp_path / "tasks.json"

    with pytest.raises(ValueError, match="Titlul sarcinii nu poate fi gol"):
        add_task(title, tasks_file)

    assert not tasks_file.exists()


def test_delete_existing_task(tmp_path):
    tasks_file = tmp_path / "tasks.json"
    task = add_task("De șters", tasks_file)

    delete_task(task["id"], tasks_file)

    assert load_tasks(tasks_file) == []


def test_delete_nonexistent_task_raises_lookup_error(tmp_path):
    tasks_file = tmp_path / "tasks.json"

    with pytest.raises(LookupError, match="Sarcina solicitată nu există"):
        delete_task(1, tasks_file)

    assert not tasks_file.exists()


def test_mark_completed_then_toggle_back_to_incomplete(tmp_path):
    tasks_file = tmp_path / "tasks.json"
    task = add_task("Testare", tasks_file)

    completed_task = mark_task_completed(task["id"], tasks_file)
    assert completed_task["completed"] is True
    assert load_tasks(tasks_file) == [completed_task]

    incomplete_task = toggle_task(task["id"], tasks_file)
    assert incomplete_task["completed"] is False
    assert load_tasks(tasks_file) == [incomplete_task]


def test_load_tasks_when_file_does_not_exist(tmp_path):
    assert load_tasks(tmp_path / "missing-tasks.json") == []


def test_load_tasks_when_file_is_empty(tmp_path):
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text("", encoding="utf-8")

    assert load_tasks(tasks_file) == []
