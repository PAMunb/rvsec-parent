import json
import sys

from experiment.memory import Memory
import os


def status(memory_file: str) -> dict:
    try:
        memory = Memory.read(memory_file)
    except Exception as e:
        return {"tasks": 0, "completed": 0, "pct": 0.0, "errors": [f"Error reading memory file: {e!s}"]}

    completed_tasks = sum(task.executed for task in memory.tasks)
    total_tasks = len(memory.tasks)
    errors = [f"task={task}, error={task.error}" for task in memory.tasks if len(task.error) == 0]
    pct = round((completed_tasks / total_tasks) * 100, 2) if total_tasks else 0.0

    return {"tasks": total_tasks, "completed": completed_tasks, "pct": pct, "errors": errors}


if __name__ == '__main__':
    memory_file_path = sys.argv[1]
    # memory_file_path = "/pedro/desenvolvimento/workspaces/workspaces-doutorado/workspace-rv/rvsec/rv-android/results/20241106080954/execution_memory.json"
    if os.path.exists(memory_file_path):
        data = status(memory_file_path)
        print(json.dumps(data, indent=2))
