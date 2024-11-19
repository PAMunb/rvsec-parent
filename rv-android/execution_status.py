import json
import sys
import time
from datetime import timedelta, datetime

import utils
from experiment.memory import Memory
import os
from experiment.task import DEFAULT_DATETIME


def status(memory_file: str) -> dict:
    try:
        memory = Memory.read(memory_file)
    except Exception as e:
        return {"tasks": 0, "completed": 0, "pct": 0.0, "errors": [f"Error reading memory file: {e!s}"]}

    completed_tasks = sum(task.executed for task in memory.tasks)
    total_tasks = len(memory.tasks)
    errors = [f"task={task}, error={task.error}" for task in memory.tasks if task.error]

    pct = round((completed_tasks / total_tasks) * 100, 2) if total_tasks else 0.0

    apks = get_apks(memory)
    tasks = get_tasks(memory)

    return {"total": total_tasks, "completed": completed_tasks, "pct": pct, "errors": errors, "tasks": tasks, "apks": apks}


def get_apks(memory: Memory):
    apks = {}
    for task in memory.tasks:
        if task.apk not in apks:
            apks[task.apk] = {
                "total_tasks": 0,
                "executed": 0,
                "pct": 0.0
            }

        executed = apks[task.apk]["executed"]
        if task.executed:
            executed = executed + 1
        total = apks[task.apk]["total_tasks"] + 1

        apks[task.apk] = {
            "total_tasks": total,
            "executed": executed,
            "pct": (executed*100)/total
        }
    return apks


def get_tasks(memory: Memory):
    tasks = []
    for task in memory.tasks:
        time: float = 0.0
        if task.executed:
            time = (task.finish_time - task.start_time).total_seconds()
        start = ""
        if task.start_time != DEFAULT_DATETIME:
            start = utils.datetime_to_string(task.start_time)
        finish = ""
        if task.finish_time != DEFAULT_DATETIME:
            finish = utils.datetime_to_string(task.finish_time)
        tasks.append({
            "task": repr(task),
            "executed": task.executed,
            "start": start,
            "finish": finish,
            "time": time
        })
    return tasks


if __name__ == '__main__':
    # memory_file_path = sys.argv[1]
    memory_file_path = "/pedro/desenvolvimento/workspaces/workspaces-doutorado/workspace-rv/rvsec/rv-android/results/20241119090210/execution_memory.json"
    if os.path.exists(memory_file_path):
        data = status(memory_file_path)
        print(json.dumps(data, indent=2))
