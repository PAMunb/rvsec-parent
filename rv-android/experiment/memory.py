# import analysis.methods_extractor as me
import json

from app import App
from experiment import config as experiment_config
from experiment.task import Task


class Memory:

    def __init__(self):
        self.tasks = set()
        self.execution_memory = {}

    def init(self, apks: list[App]):
        for apk_app in apks:
            apk = apk_app.name
            for rep in range(experiment_config.repetitions):
                repetition = rep + 1
                for timeout in experiment_config.timeouts:
                    for tool_obj in experiment_config.tools:
                        task = Task(apk, repetition, timeout, tool_obj.name)
                        self.tasks.add(task)

    def get_tasks(self, _sort=lambda x: (x.repetition, x.timeout, x.tool, x.apk)) -> list[Task]:
        sorted_tasks: list[Task]
        sorted_tasks = sorted(self.tasks, key=_sort)
        return sorted_tasks

    @staticmethod
    def read(memory_file: str):
        memory = Memory()
        with open(memory_file, 'r') as file:
            result = json.load(file)
            memory.execution_memory, memory.tasks = memory.__from_result(result)
        return memory

    def write(self, memory_file: str):
        result = self.__to_result()
        with open(memory_file, "w") as outfile:
            json.dump(result, outfile)

    def __to_result(self):
        result = {}
        for task in self.tasks:
            result.setdefault(task.apk, {}).setdefault(task.repetition, {}).setdefault(task.timeout, {})[
                task.tool] = task.executed
        return result

    @staticmethod
    def __from_result(result):
        tasks = []
        # memory = {}
        for apk, rep_data in result.items():
            # memory[apk] = {}
            for rep, timeout_data in rep_data.items():
                # memory[apk][rep] = {}
                for timeout, tool_data in timeout_data.items():
                    # memory[apk][rep][timeout] = {}
                    for tool, executed in tool_data.items():
                        task = Task(apk, rep, timeout, tool, executed)
                        # memory[apk][rep][timeout][tool] = task
                        tasks.append(task)
        # return memory, tasks
        return None, tasks

    def __str__(self):
        return "Memory=[tasks={}]".format(len(self.tasks))
