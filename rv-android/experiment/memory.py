# import analysis.methods_extractor as me
import json

from app import App
from experiment.task import Task
import utils

class Memory:

    def __init__(self):
        self.tasks = set()

    def init(self, repetitions: int, timeouts: list[int], tools: list[str], apks: list[App]):
        for apk_app in apks:
            apk = apk_app.name
            for rep in range(repetitions):
                repetition = rep + 1
                for timeout in timeouts:
                    for tool in tools:
                        task = Task(apk, repetition, timeout, tool)
                        self.tasks.add(task)

    def get_tasks(self, _sort=lambda x: (x.repetition, x.timeout, x.tool, x.apk)) -> list[Task]:
        sorted_tasks: list[Task]
        sorted_tasks = sorted(self.tasks, key=_sort)
        return sorted_tasks

    @staticmethod
    def read(memory_file: str):
        memory = Memory()
        with open(memory_file, "r") as file:
            result = json.load(file)
            memory.tasks = memory.__from_result(result)
        return memory

    def write(self, memory_file: str):
        result = self.__to_result()
        with open(memory_file, "w") as outfile:
            json.dump(result, outfile)

    def __to_result(self):
        result = {}
        for task in self.tasks:
            result.setdefault(task.apk, {}).setdefault(task.repetition, {}).setdefault(task.timeout, {})[
                task.tool] = {"executed": task.executed,
                              "start_time": task.start_time,
                              # "result": task.result,
                              # "coverage": task.coverage,
                              "error": str(task.error)
                              }
        return result

    @staticmethod
    def __from_result(result):
        tasks = []
        for apk, rep_data in result.items():
            for rep, timeout_data in rep_data.items():
                for timeout, tool_data in timeout_data.items():
                    for tool, data in tool_data.items():
                        task = Task(apk, rep, timeout, tool)
                        task.executed = data["executed"]
                        # TODO vem str, int ou datetime?
                        task.start_time = data["start_time"]
                        task.error = data["error"]
                        tasks.append(task)
        return tasks

    def __str__(self):
        return "Memory=[tasks={}]".format(len(self.tasks))
