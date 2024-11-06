import logging as logging_api
import os.path
import os.path
import shutil
from datetime import datetime

import utils
from app import App
from constants import EXTENSION_LOGCAT, EXTENSION_TRACE, EXTENSION_METHODS, EXECUTION_MEMORY_FILENAME
from experiment.memory import Memory
from experiment.task import Task
from settings import *
from tools.tool_spec import AbstractTool


logging = logging_api.getLogger(__name__)


class ExecutionManager:

    def __init__(self):
        self.memory: Memory
        self.tasks = []
        self.base_results_dir = ""
        self.memory_file = ""
        self.executed_tasks = set()
        self.start_time = datetime.now()
        self.finish_time = None

    def create_memory(self, apks: list[App], repetitions: int, timeouts: list[int], tools: list[AbstractTool],
                      memory_file: str, _sort=lambda x: (x.repetition, x.timeout, x.tool, x.apk)):
        # if the file exists, resume execution
        if os.path.exists(memory_file):
            self.base_results_dir = os.path.dirname(memory_file)
            self.memory_file = memory_file
            self.memory = self.read_memory()
        else:
            # start a new execution
            self.base_results_dir = create_results_dir()
            self.memory_file = os.path.join(self.base_results_dir, EXECUTION_MEMORY_FILENAME)
            self.memory = self.new_memory(repetitions, timeouts, tools, apks)
            self.write_memory()

        self.tasks = self.memory.get_tasks(_sort)
        self.init_executed_tasks()
        logging.info(f"Tasks: {self.statistics()}")
        logging.info(f"Execution memory file: {self.memory_file}")

    def init_executed_tasks(self):
        # self.executed_tasks = {task for task in self.tasks if task.executed}
        self.executed_tasks = set()
        for task in self.tasks:
            if task.executed:
                self.executed_tasks.add(task)

    def statistics(self) -> dict:
        pct = 0.0
        if len(self.tasks) > 0:
            pct = (len(self.executed_tasks) * 100) / len(self.tasks)
        data = {"tasks": len(self.tasks),
                "completed": len(self.executed_tasks),
                "pct": round(pct, 2)}
        return data

    def start_task(self, task: Task):
        task.start_time = datetime.now()
        results_dir = os.path.join(self.base_results_dir, task.apk)
        task.results_dir = results_dir
        utils.create_folder_if_not_exists(results_dir)
        copy_methods_file(task.apk, results_dir)
        base_name = "{0}__{1}__{2}__{3}".format(task.apk, task.repetition, task.timeout, task.tool)
        task.logcat_file = os.path.join(results_dir, "{}{}".format(base_name, EXTENSION_LOGCAT))
        task.log_file = os.path.join(results_dir, "{}{}".format(base_name, EXTENSION_TRACE))

    def finish_task(self, task):
        task.executed = True
        task.finish_time = datetime.now() - task.start_time
        self.executed_tasks.add(task)
        self.write_memory()

    def task_error(self, task, ex):
        task.error = str(ex)
        self.write_memory()

    def read_memory(self) -> Memory:
        logging.info("Reading execution memory file: {}".format(self.memory_file))
        return Memory.read(self.memory_file)

    def write_memory(self):
        logging.debug("Writing execution memory file: {}".format(self.memory_file))
        self.memory.write(self.memory_file)

    @staticmethod
    def new_memory(repetitions: int, timeouts: list[int], tools_obj: list[AbstractTool], apks: list[App]) -> Memory:
        tools = [x.name for x in tools_obj]
        logging.info("Creating new execution memory=[apks={}, repetitions={}, timeouts={}, tools={}]"
                     .format(len(apks), repetitions, timeouts, tools))
        memory = Memory()
        memory.init(repetitions, timeouts, tools, apks)
        return memory


def create_results_dir():
    results_dir = os.path.join(RESULTS_DIR, TIMESTAMP)
    utils.create_folder_if_not_exists(results_dir)
    return results_dir


def copy_methods_file(apk: str, app_results_dir: str):
    methods_file_name = apk + EXTENSION_METHODS
    methods_file = os.path.join(INSTRUMENTED_DIR, methods_file_name)
    if os.path.exists(methods_file):
        shutil.copy(methods_file, app_results_dir)
