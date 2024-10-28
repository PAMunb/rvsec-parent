import logging as logging_api
import os.path

import utils
from app import App
from experiment.memory import Memory
from experiment.task import Task
from settings import *
from tools.tool_spec import AbstractTool

EXECUTION_MEMORY_FILENAME = "execution_memory.json"

logging = logging_api.getLogger(__name__)


class ExecutionManager:
    def __init__(self):
        self.memory = None
        self.tasks = []
        self.base_results_dir = ""
        self.memory_file = ""
        self.executed_tasks = set()

    def create_memory(self, repetitions: int, timeouts: list[int], tools: list[AbstractTool], apks: list[App],
                      memory_file: str, _sort=lambda x: (x.repetition, x.timeout, x.tool, x.apk)):
        logging.info(f"Creating execution memory: {memory_file}")
        # if the file exists, resume execution
        if os.path.exists(memory_file):
            self.base_results_dir = os.path.dirname(memory_file)
            self.memory_file = memory_file
            self.memory = self.read_memory(memory_file)
        else:
            # start a new execution
            self.base_results_dir = create_results_dir()
            self.memory_file = os.path.join(self.base_results_dir, EXECUTION_MEMORY_FILENAME)
            self.memory = self.new_memory(repetitions, timeouts, tools, apks)
        self.tasks = self.memory.get_tasks(_sort)
        self.init_executed_tasks()

    def init_executed_tasks(self):
        # self.executed_tasks = {task for task in self.tasks if task.executed}
        self.executed_tasks = set()
        for task in self.tasks:
            if task.executed:
                self.executed_tasks.add(task)

    def statistics(self):
        pct = (len(self.executed_tasks) * 100) / len(self.tasks)
        data = {"tasks": len(self.tasks),
                "completed": len(self.executed_tasks),
                "pct": round(pct, 2)}
        return data

    def start_task(self, task: Task):
        task.start_time = time.time()

    def finish_task(self, task):
        task.executed = True
        task.time = time.time() - task.start_time
        self.executed_tasks.add(task)
        self.write_memory(self.memory, self.memory_file)

    @staticmethod
    def read_memory(memory_file: str):
        logging.info("Reading execution memory file: {}".format(memory_file))
        return Memory.read(memory_file)

    @staticmethod
    def write_memory(memory: Memory, memory_file: str):
        logging.info("Writing execution memory file: {}".format(memory_file))
        memory.write(memory_file)

    @staticmethod
    def new_memory(repetitions: int, timeouts: list[int], tools: list[AbstractTool], apks: list[App]):
        logging.info("Creating new execution memory=[apks={}, repetitions={}, timeouts={}, tools={}]"
                     .format(len(apks), repetitions, timeouts, list(map(lambda tool: tool.name, tools))))
        memory = Memory()
        memory.init(apks)  # repetitions, timeouts, tools, apks)
        return memory


def create_results_dir():
    results_dir = os.path.join(RESULTS_DIR, TIMESTAMP)
    utils.create_folder_if_not_exists(results_dir)
    return results_dir
